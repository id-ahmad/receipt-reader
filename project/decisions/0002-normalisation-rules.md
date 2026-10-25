---
status: accepted
date: 2026-10-25
owner: Abdel
---

# 0002 — Normalisation rules: amounts, counts, discount sign

## Context

ADR 0001 fixed the fields and said amounts become whole rupiah, but not how to read the
strings, nor the type of an item's count. A survey of one training shard (200 receipts,
1,592 values) found 45 distinct formats: `43,636`, `25.000`, `9.500,00`, `181,500.00`,
`19 000`, `Rp 35,636.36`, `TOTAL 47,499`, discounts written `-300`, `39,800)` or `(0)`,
and counts written `2X`, `x1`, `1.0`, `*2`, `0.512X`.

## Decision

1. **Amounts:** strip everything except digits and separators (`.` `,` space), keeping
   whether there was a minus sign or parentheses. Then the **last separator decides**:
   exactly 3 digits after it → it groups thousands; 1 or 2 digits → it's the decimal point.
   Earlier separators must each be followed by exactly 3 digits; any other shape is
   rejected with an error rather than guessed. Round half up to whole rupiah.
2. **Counts:** a decimal number, not an integer. Strip `x`, `X`, `*`, and read any separator
   as a decimal point (`0.512X` → `0.512`).
3. **Discount:** stored as a positive amount, subtracted in the arithmetic checks.
4. **No digits at all** (e.g. tax `-`) → `null`.

## Why

- Comma or dot doesn't matter, only position, so one rule covers both the European
  (`9.500,00`) and English (`181,500.00`) styles.
- The 3-digit rule is safe **because the currency is rupiah**: no price is a few rupiah,
  and rupiah is never written with 3 decimals. In a 3-decimal currency (e.g. the Kuwaiti
  dinar) it would silently misread amounts. This assumption must stay written down.
- Counts can't use the amount rule: `0.512X` (an item sold by weight) would become 512.
  The same string means different things in different fields, so normalisation is per field.
- CORD's discount signs are inconsistent, so the sign carries no reliable meaning; the
  field name already says it's a reduction.
- Rejecting unknown shapes surfaces surprises instead of hiding them in the scores.

## Consequences

- `count` is a decimal in the schema; scoring compares counts as numbers.
- Every rejected string is reported by the ground-truth survey and handled explicitly.

## Alternatives considered

- **One normalisation function for every field** — breaks on counts (`0.512X` → 512).
- **Keep the discount's sign as written** — inconsistent in CORD, so scores would penalise
  the sign convention, not the reading.
- **Guess on unknown shapes** (e.g. drop all separators) — silently wrong values in the
  ground truth, which is worse than a loud failure.
