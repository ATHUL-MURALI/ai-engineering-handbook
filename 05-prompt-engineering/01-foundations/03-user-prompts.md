# User Prompts

## What it is

The user prompt is the **per-request payload**: the question plus the data needed
to answer it. If the system prompt is the function signature, the user prompt is
the arguments.

## The shape of a good user prompt

```
<task>Summarise the meeting for the CFO.</task>

<transcript>
...raw data...
</transcript>

<focus>Budget decisions and any dates committed to.</focus>
```

Three habits do most of the work:

1. **Wrap data in delimiters** — XML-ish tags are the clearest for current models.
2. **State the goal, not just the data** — "summarise for the CFO" beats "summarise".
3. **Put the question after long data** for very long inputs; models attend
   strongly to the end of the context. For short inputs, question-first is fine.

## Multi-turn user prompts

In a chat, the `messages` list *is* the prompt. Each turn is
`{"role": "user" | "assistant", "content": ...}`. You control this list, so you
control history: you can trim it, summarise it, or drop irrelevant turns. The model
has no memory beyond what you resend.

## Key points

- Never build a user prompt by naive f-string concatenation of untrusted text
  without delimiters — that is how injection happens.
- One question per turn. If the user asks three things, you can still split them
  into three calls and merge the answers.
- Include *negative* context when it helps: "The user is on the free plan, so do
  not suggest paid-only features."

## Gotchas

- Users write terrible prompts. Production systems usually *rewrite* the user's
  message before it reaches the model (see *query rewriting*).
- Don't stuff the whole conversation history in every call forever — cost grows
  quadratically and quality drops (see *context-window management*).
- Empty or whitespace-only user content errors out on some providers. Validate.

## Try it yourself

Run the example, then change `focus` to "Only the action items with owners" and see
how much the answer changes while the data stays identical.
