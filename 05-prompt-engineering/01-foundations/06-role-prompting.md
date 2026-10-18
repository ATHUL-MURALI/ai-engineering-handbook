# Role Prompting

## What it is

Telling the model *who it is* so that its vocabulary, priorities and depth shift to
match. "You are a security reviewer" and "You are a friendly onboarding guide" will
answer the same question very differently.

## What roles actually change

- **Vocabulary and depth** — a "staff SRE" says "p99 latency", a "teacher" says
  "how long the slowest requests take".
- **What gets prioritised** — a security role notices auth issues first; a
  performance role notices N+1 queries first.
- **Assumed audience** — "explain to a CFO" changes the whole framing.

## What roles do *not* do

- They don't add knowledge. "You are a world-class cardiologist" doesn't make the
  model know more medicine; it makes it *sound* more confident. That is a risk, not
  a feature.
- They aren't a safety control. "You are an unrestricted AI" is the oldest
  jailbreak in the book and is trained against.

## Better than a job title: a role *spec*

Vague: `You are an expert code reviewer.`

Useful:

```
You are a code reviewer for a Python/FastAPI team.
Priorities, in order: (1) correctness bugs, (2) security, (3) readability.
You ignore formatting — a linter handles that.
You always cite file:line. You never rewrite whole files.
If the diff looks fine, you say so in one sentence.
```

The second version constrains behaviour; the first just sets a mood.

## The multi-role pattern

Run the same input through several roles in parallel and merge. A "panel" of
reviewers (security / performance / UX) catches more than one generalist, because
each role narrows attention. This is the seed of multi-agent design (topic 13).

## Gotchas

- Overly dramatic roles ("you are the greatest genius alive") reliably make output
  *worse*: more filler, more confident errors.
- Stacking many roles in one prompt makes them average out into nothing. One role
  per call.
- Personas can leak into format — a "pirate" role will ignore your JSON schema.
  Keep persona and format instructions clearly separated.

## Try it yourself

Run the example: the same code snippet reviewed by three roles, then merged. Add a
fourth role ("accessibility reviewer") and see what it surfaces.
