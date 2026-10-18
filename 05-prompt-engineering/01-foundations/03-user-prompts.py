"""User prompts: delimited data + explicit goal, and multi-turn history.

Run:  python 03-user-prompts.py
Needs: OPENAI_API_KEY
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM = "You are a precise meeting analyst. Never invent facts not in the transcript."

TRANSCRIPT = """
Ana: We're 12% over on cloud spend.
Ravi: Most of it is the staging cluster running 24/7.
Ana: Can we shut staging down at night?
Ravi: Yes. I'll ship the scheduler by March 14.
Ana: Good. I'll tell finance we save ~8k/quarter.
Priya: Also, the vendor contract renews April 1, we should renegotiate.
"""


def build_user_prompt(transcript: str, task: str, focus: str) -> str:
    """Goal first, data in delimiters, focus last (closest to generation)."""
    return (
        f"<task>{task}</task>\n\n"
        f"<transcript>\n{transcript.strip()}\n</transcript>\n\n"
        f"<focus>{focus}</focus>"
    )


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY in .env first.")

    client = OpenAI()

    # ---- single turn ------------------------------------------------------
    user_prompt = build_user_prompt(
        TRANSCRIPT,
        task="Summarise this meeting for the CFO in 3 bullets.",
        focus="Budget impact and any dates people committed to.",
    )
    print("USER PROMPT:\n" + user_prompt + "\n" + "=" * 70)

    first = client.responses.create(
        model="gpt-4.1-mini", instructions=SYSTEM, input=user_prompt, temperature=0.2
    )
    print("TURN 1:\n" + first.output_text)

    # ---- multi turn: the messages list IS the prompt ----------------------
    # With the Responses API you can either resend the list, or pass
    # previous_response_id and let the server keep the history.
    followup = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM,
        input="Now list only the commitments with an owner and a date, as a table.",
        previous_response_id=first.id,  # server-side conversation state
    )
    print("\n" + "=" * 70 + "\nTURN 2:\n" + followup.output_text)


if __name__ == "__main__":
    main()
