---
status: accepted
date: 2026-10-26
owner: Abdel
---

# 0003 — Ground-truth fixes: structural rules plus a corrections file

## Context

Running the ADR 0002 rules over all 800 training receipts converted 785. The 15 failures
were of three kinds:
- labelling typos (`Rp 57,0000` where the photo shows `Rp57,000`);
- extra text in a value (`Pb1 10% 7,000`);
- structural surprises: items with no name, names labelled as several pieces, two
  `sub_total` blocks, a stray trailing dot in a count, and one name typed into the
  count field.

## Decision

- **Recurring patterns get a rule in the converter:**
  - a missing item name becomes `""`, keeping the item, whose count and price are real;
  - a name in several pieces is joined with spaces;
  - several `sub_total` blocks are merged, with the first value of each field winning
    (the first block is before discount, matching the subtotal definition);
  - stray separators at the ends of a count are ignored.
- **One-off label errors go in `src/receipt_reader/cord_corrections.json`**: split, index,
  path, the raw value expected, the fixed raw value, and the reason (usually "the photo
  shows …"). The original dataset is never edited. A correction whose expected raw value
  doesn't match fails loudly.
- **The dataset is pinned** to Hugging Face revision `7f0115a4…`, because indices and
  corrections refer to that exact version.

## Why

A rule pays off when the case recurs and can be tested. Handling `Pb1 10% 7,000` with a
rule would add tricky code for 2 values out of 5,815. A documented patch is simpler and
shows its evidence.

## Consequences

- Train: 800/800 receipts convert, with 6 corrections on 5 receipts. Validation: 100/100,
  with no corrections and no new rejections, so the rules held on data they weren't
  designed on.
- The test split's ground truth gets converted only for the final run. If it raises, the
  failing label is fixed the same way (a documented correction) without looking at
  anything else in the test set.

## Alternatives considered

- **Extend the amount rule to strip tax names and rates** — tricky regexes for two values,
  with a risk of breaking other cases (`RP36362`).
- **Drop the failing receipts** — throws away 15 of 800 receipts for problems that are
  fixable, and drops exactly the messy cases the systems must handle.
