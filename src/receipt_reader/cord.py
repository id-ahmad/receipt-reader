"""Load CORD v2 and convert its ground truth into the target schema."""

import json
from collections.abc import Iterator
from functools import cache
from pathlib import Path
from typing import Any

import datasets

from receipt_reader.normalise import parse_amount, parse_count
from receipt_reader.schema import Item, Receipt

DATASET = "naver-clova-ix/cord-v2"
# Pinned like a code dependency: receipt indices and corrections refer to this exact version.
DATASET_REVISION = "7f0115a4b758a71d6473b8d085751692da2fef98"
SPLITS = ("train", "validation", "test")
CORRECTIONS_FILE = Path(__file__).with_name("cord_corrections.json")


def load_split(split: str) -> datasets.Dataset:
    """Download (first call only, then cached) and return one split."""
    if split not in SPLITS:
        raise ValueError(f"unknown split {split!r}, expected one of {SPLITS}")
    dataset = datasets.load_dataset(DATASET, split=split, revision=DATASET_REVISION)
    assert isinstance(dataset, datasets.Dataset)
    return dataset


def iter_gt_parse(split: str) -> Iterator[tuple[int, dict[str, Any]]]:
    """Yield (index, `gt_parse`) for each receipt, corrections applied, images not decoded."""
    for index, row in enumerate(load_split(split).select_columns(["ground_truth"])):
        parse: dict[str, Any] = json.loads(row["ground_truth"])["gt_parse"]
        yield index, apply_corrections(split, index, parse)


def iter_ground_truth(split: str) -> Iterator[tuple[int, Receipt]]:
    """Yield (index, Receipt) for each receipt of a split."""
    for index, parse in iter_gt_parse(split):
        yield index, convert_ground_truth(parse)


@cache
def _corrections() -> list[dict[str, Any]]:
    corrections: list[dict[str, Any]] = json.loads(CORRECTIONS_FILE.read_text())
    return corrections


def apply_corrections(
    split: str,
    index: int,
    gt_parse: dict[str, Any],
    corrections: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Replace known-bad raw labels with what the receipt actually shows.

    Each correction names the raw value it expects, so if the dataset ever changes under
    us, the correction fails loudly instead of overwriting the wrong value.
    """
    for fix in _corrections() if corrections is None else corrections:
        if fix["split"] != split or fix["index"] != index:
            continue
        *parents, key = fix["path"]
        target = gt_parse
        for parent in parents:
            target = target[parent]
        if target.get(key) != fix["raw"]:
            raise ValueError(
                f"correction for {split}[{index}] {fix['path']} expected {fix['raw']!r}, "
                f"found {target.get(key)!r}"
            )
        target[key] = fix["fixed"]
    return gt_parse


def convert_ground_truth(gt_parse: dict[str, Any]) -> Receipt:
    """Convert one CORD `gt_parse` into a Receipt. Raises on shapes it doesn't know."""
    menu = gt_parse.get("menu", [])
    if isinstance(menu, dict):  # single-item receipts store one object, not a list
        menu = [menu]
    sub_total = _section(gt_parse, "sub_total")
    total = _section(gt_parse, "total")
    discount = _amount(sub_total.get("discount_price"))
    return Receipt(
        items=[_item(entry) for entry in menu],
        subtotal=_amount(sub_total.get("subtotal_price")),
        tax=_amount(sub_total.get("tax_price")),
        service=_amount(sub_total.get("service_price")),
        discount=abs(discount) if discount is not None else None,
        total=_amount(total.get("total_price")),
    )


def _section(gt_parse: dict[str, Any], key: str) -> dict[str, Any]:
    section = gt_parse.get(key, {})
    if isinstance(section, list):  # several blocks (e.g. subtotal before and after discount)
        merged: dict[str, Any] = {}
        for block in section:
            for field, value in block.items():
                merged.setdefault(field, value)  # the first block's value wins
        return merged
    if not isinstance(section, dict):
        raise TypeError(f"{key} is a {type(section).__name__}, expected an object")
    return section


def _item(entry: dict[str, Any]) -> Item:
    name = entry.get("nm")
    if name is None:  # name unreadable on the receipt; count and price are still real
        name = ""
    elif isinstance(name, list):  # the line's text was labelled as several pieces
        name = " ".join(str(piece) for piece in name)
    elif not isinstance(name, str):
        raise TypeError(f"item name is {name!r}, expected a string")
    count = entry.get("cnt")
    if count is not None and not isinstance(count, str):
        raise TypeError(f"item count is {count!r}, expected a string")
    return Item(
        name=name.strip(),
        count=parse_count(count) if count is not None else None,
        price=_amount(entry.get("price")),
    )


def _amount(raw: Any) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, list):  # several lines of one kind (e.g. two tax lines): add them up
        parts = [part for part in (_amount(value) for value in raw) if part is not None]
        return sum(parts) if parts else None
    if not isinstance(raw, str):
        raise TypeError(f"amount is {raw!r}, expected a string")
    return parse_amount(raw)
