"""Run the normalisation rules over every ground-truth value of a split and report.

Shows, for each format of amount and count (digits replaced by 9), one raw example and
what the rules turned it into, plus every value and receipt the rules rejected.
Corrections from cord_corrections.json are applied first.

    uv run python scripts/survey_ground_truth.py [train|validation]

The test split is refused: it is only touched for final numbers.
"""

import re
import sys
from collections import Counter
from collections.abc import Callable, Iterator
from typing import Any

from receipt_reader.cord import convert_ground_truth, iter_gt_parse
from receipt_reader.normalise import parse_amount, parse_count

AMOUNT_FIELDS = {
    "sub_total": ["subtotal_price", "tax_price", "service_price", "discount_price"],
    "total": ["total_price"],
}


def raw_values(parse: dict[str, Any]) -> Iterator[tuple[str, Any]]:
    """Yield (field, raw value) for every field in the target schema."""
    menu = parse.get("menu", [])
    for entry in [menu] if isinstance(menu, dict) else menu:
        if isinstance(entry, dict):
            yield "item price", entry.get("price")
            yield "item count", entry.get("cnt")
    for section, keys in AMOUNT_FIELDS.items():
        values = parse.get(section)
        if isinstance(values, dict):
            for key in keys:
                yield key, values.get(key)


def main() -> None:
    split = sys.argv[1] if len(sys.argv) > 1 else "train"
    if split == "test":
        sys.exit("refusing to survey the test split: it is only touched for final numbers")

    shapes: Counter[tuple[str, str]] = Counter()
    examples: dict[tuple[str, str], tuple[str, Any]] = {}
    rejected_values: list[tuple[int, str, Any, str]] = []
    rejected_receipts: list[tuple[int, str]] = []
    receipts = 0

    for index, parse in iter_gt_parse(split):
        receipts += 1
        try:
            convert_ground_truth(parse)
        except (TypeError, ValueError) as error:
            rejected_receipts.append((index, f"{type(error).__name__}: {error}"))

        for field, raw in raw_values(parse):
            if raw is None:
                continue
            kind = "count" if field == "item count" else "amount"
            parser: Callable[[str], Any] = parse_count if kind == "count" else parse_amount
            if not isinstance(raw, str):
                key = (kind, f"<{type(raw).__name__}>")
                shapes[key] += 1
                examples.setdefault(key, (repr(raw), "handled by the converter"))
                continue
            key = (kind, re.sub(r"\d", "9", raw))
            shapes[key] += 1
            try:
                examples.setdefault(key, (raw, parser(raw)))
            except ValueError as error:
                rejected_values.append((index, field, raw, str(error)))

    print(f"split={split} receipts={receipts} values={sum(shapes.values())} formats={len(shapes)}")
    print(f"\nreceipts the converter rejected: {len(rejected_receipts)}")
    for index, message in rejected_receipts:
        print(f"  receipt {index}: {message}")
    print(f"\nvalues the rules rejected: {len(rejected_values)}")
    for index, field, raw, message in rejected_values:
        print(f"  receipt {index} {field}: {raw!r} ({message})")
    for kind in ("amount", "count"):
        print(f"\n{kind} formats (count, format, example -> parsed):")
        for (k, shape), n in shapes.most_common():
            if k == kind:
                raw, parsed = examples.get((k, shape), ("?", "rejected"))
                print(f"  {n:5d}  {shape!r:24} {raw!r} -> {parsed!r}")


if __name__ == "__main__":
    main()
