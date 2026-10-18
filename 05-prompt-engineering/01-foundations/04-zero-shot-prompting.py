"""Zero-shot prompting: three strengths of the same zero-example prompt.

Run:  python 04-zero-shot-prompting.py
Needs: OPENAI_API_KEY
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

REVIEWS = [
    "Arrived two days late but honestly the fabric is beautiful.",
    "Does exactly what it says. Nothing more to add.",
    "I asked support three times and nobody replied, so I returned it.",
]

# 1. Plain zero-shot: just describe the task.
PLAIN = """Classify the review sentiment as positive, negative or neutral.
Answer with one word."""

# 2. Zero-shot + label definitions + escape hatch. Still zero examples.
DEFINED = """Classify the review sentiment. Answer with one word.

Labels:
- positive: the reviewer would recommend the product overall.
- negative: the reviewer regrets the purchase or warns others.
- neutral: factual, no clear recommendation either way.
- mixed: clear praise AND clear complaint, roughly balanced.

If nothing fits, answer: unknown."""

# 3. Zero-shot + reasoning. Costs tokens, helps on ambiguous input.
REASONED = """Classify the review sentiment.

First write "Reasoning:" and one short sentence.
Then write "Label:" followed by exactly one of: positive, negative, neutral, mixed."""


def ask(client: OpenAI, system: str, review: str) -> str:
    return client.responses.create(
        model="gpt-4.1-mini",
        instructions=system,
        input=f"<review>{review}</review>",
        temperature=0,  # classification: no creativity wanted
    ).output_text.strip()


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY in .env first.")

    client = OpenAI()
    for label, prompt in [("PLAIN", PLAIN), ("DEFINED", DEFINED), ("REASONED", REASONED)]:
        print("=" * 70)
        print(label)
        for review in REVIEWS:
            answer = ask(client, prompt, review).replace("\n", " | ")
            print(f"  {review[:45]:<47} -> {answer}")


if __name__ == "__main__":
    main()
