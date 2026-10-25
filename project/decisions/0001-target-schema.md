---
status: accepted
date: 2026-10-25
owner: Abdel
---

# 0001 — Target schema: which fields count and how amounts are normalised

## Context

Every system (OCR baseline, open-weight vision model, Claude, router) is scored against one
target schema, so it has to be fixed before anything is built.

CORD v2's `gt_parse` has about 30 field types under `menu`, `void_menu`, `sub_total` and
`total`, and many are rare. In one training shard (200 receipts), `total_price` appears on
199, `subtotal_price` on 141, `tax_price` on 99, `service_price` on 30 and `discount_price`
on 16. Store and payment info were removed from the public release.

Amounts in the ground truth are strings in mixed formats, sometimes within one receipt:
`"43,636"`, `"6.000"`, `"9.500,00"`, even `"TOTAL 47,499"`.

## Decision

**Fields scored:**
- Per item: name (`nm`), count (`cnt`), line price (`price`).
- Per receipt: `subtotal_price`, `tax_price`, `service_price`, `discount_price`, `total_price`.

**Amounts:** normalised to integers in rupiah. `"43,636"`, `"6.000"` and `"9.500,00"` become
`43636`, `6000` and `9500`.

## Why

- These are the fields a real user of the output needs: what was bought, and what was paid
  in total, tax included.
- They are exactly the fields the router's arithmetic checks use: items add up to the
  subtotal; subtotal − discount + service + tax ≈ total.
- Normalising amounts means the score measures *reading* the receipt, not matching the
  annotator's formatting.

## Consequences

- The data loader must parse every amount format found in the ground truth into an integer,
  and must handle `menu` being a single object instead of a list.
- Still to decide while building scoring: how item names are compared (exact vs ignoring
  case and spacing), how an item with no `cnt` is treated, and how items are matched
  between prediction and ground truth.
- Rare fields (`discount_price`) will have noisy per-field scores; report how many receipts
  each field's score is based on.

## Alternatives considered

- **All CORD fields** — closer to published work (e.g. Donut), but many fields are too rare
  to score reliably, and they add work without adding learning.
- **Also cash and change** (`cashprice`, `changeprice`) — would enable a third check
  (cash − total = change), but they describe the payment, not the purchase.
- **Keep amounts as strings** — a correct `43636` would be marked wrong against `"43,636"`.
