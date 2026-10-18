# Prompt Structure

## What it is

A prompt is not one blob of text. It is a small document with sections. Models pay
attention to structure the same way a reader does: headings, delimiters and order
tell the model what each piece of text *is for*.

The six-part skeleton that works for almost every task:

```
1. ROLE      "You are a senior support engineer."
2. TASK      "Classify the ticket into exactly one category."
3. CONTEXT   The ticket text, docs, retrieved chunks — inside delimiters.
4. RULES     "Never guess. If unsure, use 'other'."
5. EXAMPLES  Two or three input → output pairs.
6. FORMAT    "Reply with JSON: {"category": ..., "confidence": ...}"
```

## Why the order matters

- **Instructions before data.** The model reads left to right; if the rules come
  first it knows what to look for while reading the data.
- **Format last.** It is the last thing in context before generation starts, so it
  has the strongest pull on the first tokens the model writes.
- **Delimiters around data.** `<ticket>...</ticket>` or triple backticks make it
  unambiguous where user data stops and your instructions resume. This is also the
  first line of defence against prompt injection.

## Key points

- One task per prompt. Two tasks = two prompts (see *prompt chaining*).
- Positive instructions beat negative ones: "use category `other`" works better
  than "don't make up categories".
- Be specific about *scale*: "3–5 bullet points, max 15 words each" not "be brief".
- Keep the skeleton stable and only swap the variable parts — that is what makes a
  prompt *template*.

## Gotchas

- A wall of text with no delimiters is the #1 cause of the model "following"
  instructions that were actually inside user data.
- Very long rule lists (20+) start to conflict with each other. Group them, or
  split the task.
- Don't put the output format in the middle and then add more context after it.

## Try it yourself

Run the example, then delete the RULES section and re-run. Notice how the model
starts inventing categories.
