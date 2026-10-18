# Few-Shot Prompting

## What it is

Show the model **1–5 worked examples** of input → output before giving it the real
input. The model infers the pattern from the demonstrations. Nothing is trained;
the examples just live in the context window.

```
Input: "charged twice"        Output: {"cat": "billing"}
Input: "export button spins"  Output: {"cat": "bug"}
Input: "how do I invite?"     Output:            <- model completes this
```

## Why it works so well

Examples communicate things that are painful to describe in prose: tone, level of
detail, edge-case handling, exact formatting, how to handle nulls. One good example
often replaces a paragraph of rules.

## How to choose examples

- **Cover the boundaries**, not the obvious middle. Include the case you keep
  getting wrong.
- **Balance the labels.** If 4 of 5 examples are `billing`, the model over-predicts
  `billing`. This is called recency/majority label bias.
- **Keep format byte-identical** across examples. Any inconsistency becomes noise.
- **3–5 is the sweet spot** for most tasks. Beyond ~8 the gains flatten and cost
  rises.
- Put examples in the **user turn** (or a fake assistant turn), not buried in the
  middle of the system rules.

## Multi-turn ("chat-style") few-shot

Instead of one text block, encode examples as real message turns:

```python
messages = [
    {"role": "system", "content": RULES},
    {"role": "user", "content": "charged twice"},
    {"role": "assistant", "content": '{"cat":"billing"}'},
    {"role": "user", "content": "export button spins"},
    {"role": "assistant", "content": '{"cat":"bug"}'},
    {"role": "user", "content": real_input},
]
```

This is usually the strongest form on chat models, because it matches how they were
trained.

## Dynamic few-shot (the production pattern)

Keep a pool of 50–500 labelled examples. At request time, retrieve the *k* most
similar examples to the current input (embedding similarity) and inject only those.
You get few-shot accuracy with a prompt that adapts to each input. LangChain calls
this a `SemanticSimilarityExampleSelector`.

## Gotchas

- Examples eat your cache-friendly prefix if they change every call. Put static
  examples early, dynamic ones late.
- Wrong examples are worse than no examples — the model copies your mistakes.
- With structured outputs enabled, examples should teach *content decisions*, not
  format; the schema handles format.

## Try it yourself

Run the example: zero-shot vs static few-shot vs dynamic (similarity-selected)
few-shot on the same inputs.
