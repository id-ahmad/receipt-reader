"""Turn amount and count strings into numbers (ADR 0002).

Amounts: the last separator decides. Exactly 3 digits after it means it groups thousands;
1 or 2 digits means it's the decimal point. Safe for rupiah, which is never written with
3 decimals. Results are whole rupiah, rounded half up.

Counts: any separator is a decimal point ("0.512X" is 0.512 kg, not 512).
"""

import re
from decimal import ROUND_HALF_UP, Decimal

_DIGIT = re.compile(r"\d")
_SEPARATORS = re.compile(r"[.,\s]+")


def parse_amount(raw: str) -> int | None:
    """Return the amount in whole rupiah, or None if the string holds no digits.

    Signed: "-300" and "(300)" are negative. Raises ValueError on a shape the rule
    doesn't cover, rather than guessing.
    """
    if not _DIGIT.search(raw):
        return None
    negative = any(sign in raw for sign in "-()")
    core = re.sub(r"[^\d.,\s]", "", raw).strip(" .,")
    groups = _SEPARATORS.split(core)

    whole, fraction = groups, ""
    if len(groups) > 1 and len(groups[-1]) in (1, 2):
        whole, fraction = groups[:-1], groups[-1]
    if any(len(group) != 3 for group in whole[1:]):
        raise ValueError(f"unrecognised amount format: {raw!r}")

    value = Decimal("".join(whole) + (f".{fraction}" if fraction else ""))
    rupiah = int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))
    return -rupiah if negative else rupiah


def parse_count(raw: str) -> float | None:
    """Return the quantity as a number, or None if the string holds no digits."""
    if not _DIGIT.search(raw):
        return None
    core = re.sub(r"[^\d.,\s]", "", raw).strip(" .,")
    if re.search(r"\s", core) or core.count(".") + core.count(",") > 1:
        raise ValueError(f"unrecognised count format: {raw!r}")
    return float(core.replace(",", "."))
