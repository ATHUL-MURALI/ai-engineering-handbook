"""Few-shot prompting: static examples, chat-style examples, and dynamic selection.

Run:  python 05-few-shot-prompting.py
Needs: OPENAI_API_KEY
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM = (
    "You convert a customer sentence into an internal ticket tag. "
    "Reply with the tag only, lowercase, snake_case. Tags are company-specific."
)

# A pool of labelled examples. In production this lives in a DB or a JSON file.
EXAMPLE_POOL: list[tuple[str, str]] = [
    ("I was charged twice this month", "billing_duplicate_charge"),
    ("Please cancel my subscription", "billing_churn_risk"),
    ("The CSV export never finishes", "bug_export_timeout"),
    ("Dark mode looks broken on mobile", "bug_ui_mobile"),
    ("Can you add SSO with Okta?", "feature_sso"),
    ("How do I invite a teammate?", "howto_team_invite"),
    ("Where do I download my invoice?", "howto_invoice"),
]

TEST_INPUTS = [
    "My card got billed two times for January",
    "The report download hangs at 90%",
    "Do you support SAML login?",
]


def zero_shot(client: OpenAI, text: str) -> str:
    return client.responses.create(
        model="gpt-4.1-mini", instructions=SYSTEM, input=text, temperature=0
    ).output_text.strip()


def few_shot_chat(client: OpenAI, text: str, examples: list[tuple[str, str]]) -> str:
    """Chat-style few-shot: examples become real user/assistant turns."""
    turns: list[dict[str, str]] = []
    for user_text, tag in examples:
        turns.append({"role": "user", "content": user_text})
        turns.append({"role": "assistant", "content": tag})
    turns.append({"role": "user", "content": text})

    return client.responses.create(
        model="gpt-4.1-mini", instructions=SYSTEM, input=turns, temperature=0
    ).output_text.strip()


def select_similar(client: OpenAI, text: str, k: int = 3) -> list[tuple[str, str]]:
    """Dynamic few-shot: embed the pool + the query, keep the k nearest examples."""
    import numpy as np

    texts = [e[0] for e in EXAMPLE_POOL] + [text]
    res = client.embeddings.create(model="text-embedding-3-small", input=texts)
    vecs = np.array([d.embedding for d in res.data])
    pool, query = vecs[:-1], vecs[-1]
    # embeddings from this model are already L2-normalised -> dot == cosine
    scores = pool @ query
    top = np.argsort(-scores)[:k]
    return [EXAMPLE_POOL[i] for i in top]


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY in .env first.")

    client = OpenAI()
    for text in TEST_INPUTS:
        print("=" * 70)
        print(f"INPUT: {text}")
        print(f"  zero-shot        -> {zero_shot(client, text)}")
        print(f"  static few-shot  -> {few_shot_chat(client, text, EXAMPLE_POOL[:4])}")

        chosen = select_similar(client, text, k=3)
        print(f"  dynamic examples : {[c[1] for c in chosen]}")
        print(f"  dynamic few-shot -> {few_shot_chat(client, text, chosen)}")


if __name__ == "__main__":
    main()
