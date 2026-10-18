"""System prompts: same question, three different system prompts.

Run:  python 02-system-prompts.py
Needs: OPENAI_API_KEY
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

QUESTION = "Our orders table query got slow. What should I check?"

SYSTEM_PROMPTS = {
    "terse-dba": (
        "You are a PostgreSQL DBA. Answer in at most 4 numbered steps. "
        "Each step is one imperative sentence. No preamble, no pleasantries."
    ),
    "teacher": (
        "You are a patient teacher for junior developers. Explain the *why* before "
        "the *how*. Use a short analogy. Max 120 words."
    ),
    "strict-json": (
        "You are a diagnostics API. Reply with JSON only: "
        '{"checks": [{"step": string, "command": string}]}. '
        "No markdown fences, no commentary."
    ),
}


def ask(client: OpenAI, system: str, question: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=system,  # <-- the system prompt lives here
        input=question,  # <-- the user prompt
        temperature=0.2,
    )
    return response.output_text


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY in .env first.")

    client = OpenAI()
    for name, system in SYSTEM_PROMPTS.items():
        print("=" * 70)
        print(f"SYSTEM PROMPT: {name}")
        print("-" * 70)
        print(ask(client, system, QUESTION))
        print()


if __name__ == "__main__":
    main()
