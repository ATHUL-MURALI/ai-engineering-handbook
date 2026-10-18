"""Role prompting: a review panel. Three roles look at one snippet, then merge.

Run:  python 06-role-prompting.py
Needs: OPENAI_API_KEY
"""

import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

SNIPPET = '''
@app.get("/users/{user_id}/orders")
async def orders(user_id: str, db=Depends(get_db)):
    rows = await db.fetch(f"SELECT * FROM orders WHERE user_id = '{user_id}'")
    out = []
    for r in rows:
        user = await db.fetchrow("SELECT * FROM users WHERE id = $1", r["user_id"])
        out.append({"order": dict(r), "user": dict(user)})
    return out
'''

# A role is a *spec*: identity + priorities + what to ignore + output shape.
ROLES = {
    "security": (
        "You are an application security reviewer for a Python/FastAPI team.\n"
        "Priorities: injection, authz/authn, data exposure. Ignore style.\n"
        "Output: max 3 bullets, each 'ISSUE - why it matters - fix in one line'."
    ),
    "performance": (
        "You are a backend performance engineer.\n"
        "Priorities: query count, N+1 patterns, payload size, blocking calls.\n"
        "Output: max 3 bullets, each 'ISSUE - measured impact - fix in one line'."
    ),
    "api-design": (
        "You are an API designer who cares about contracts and clients.\n"
        "Priorities: response shape, status codes, pagination, typing. Ignore security.\n"
        "Output: max 3 bullets, each 'ISSUE - client pain - fix in one line'."
    ),
}

MERGE_ROLE = (
    "You are a tech lead. You receive three specialist reviews of one snippet.\n"
    "Deduplicate, then output the top 3 actions ordered by risk. "
    "One line each, prefixed with the owning concern in [brackets]."
)


async def review(client: AsyncOpenAI, role_name: str, role_prompt: str) -> tuple[str, str]:
    res = await client.responses.create(
        model="gpt-4.1-mini",
        instructions=role_prompt,
        input=f"<code>{SNIPPET}</code>",
        temperature=0.2,
    )
    return role_name, res.output_text.strip()


async def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY in .env first.")

    client = AsyncOpenAI()

    # Roles are independent -> run them concurrently.
    results = await asyncio.gather(*(review(client, n, p) for n, p in ROLES.items()))

    combined = ""
    for name, text in results:
        print("=" * 70)
        print(f"[{name}]\n{text}")
        combined += f"\n<review role='{name}'>\n{text}\n</review>\n"

    merged = await client.responses.create(
        model="gpt-4.1-mini", instructions=MERGE_ROLE, input=combined, temperature=0.2
    )
    print("=" * 70)
    print("MERGED PLAN\n" + merged.output_text.strip())


if __name__ == "__main__":
    asyncio.run(main())
