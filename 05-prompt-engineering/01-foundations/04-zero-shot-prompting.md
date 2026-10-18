# Zero-Shot Prompting

## What it is

Ask the model to do the task with **no examples** — just a clear description.
"Zero shot" = zero demonstrations.

```
Classify the sentiment of this review as positive, negative or neutral.
Review: "Arrived late but the quality is great."
```

Modern instruction-tuned models are surprisingly good at this. Zero-shot should
always be your **first attempt**, because it is the cheapest prompt you can write:
no examples to maintain, fewest tokens, fastest.

## When zero-shot is enough

- The task is common (summarise, translate, classify sentiment, extract emails).
- The output format is simple or enforced by a schema.
- The label set is self-explanatory from its names.

## When it breaks

- Your labels have **domain-specific meanings** ("escalation" means something
  particular at your company).
- You need a **specific style** that is hard to describe but easy to show.
- Edge cases matter and the model keeps guessing wrong on them.

That is your cue to move to few-shot.

## Making zero-shot stronger without examples

1. **Define the labels.** `urgent = customer is blocked right now` beats `urgent`.
2. **Add an escape hatch.** "If none apply, output `unknown`." This alone kills
   most hallucinated labels.
3. **Ask for reasoning first, answer last** — "think step by step, then give the
   final label on the last line". Costs tokens, buys accuracy on hard tasks.
4. **Constrain the output** with a schema so format errors disappear.

## Gotchas

- Zero-shot + `temperature=1` on a classification task will drift. Use `0`.
- "Think step by step" on a trivial task just wastes tokens and can *hurt*.
- If a reasoning model is available, zero-shot + reasoning often beats
  few-shot + a small model, for less total effort.

## Try it yourself

Run the example. It shows plain zero-shot, zero-shot with label definitions, and
zero-shot with reasoning. Compare on the deliberately ambiguous 3rd review.
