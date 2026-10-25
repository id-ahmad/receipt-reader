import pytest

from receipt_reader.normalise import parse_amount, parse_count


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        # 3 digits after the last separator: it groups thousands
        ("43,636", 43636),
        ("25.000", 25000),
        ("1,065,000", 1065000),
        ("1.065.000", 1065000),
        ("19 000", 19000),
        # 1 or 2 digits after the last separator: it's the decimal point
        ("9.500,00", 9500),
        ("181,500.00", 181500),
        ("39,200.0", 39200),
        ("39,200,00", 39200),
        ("0,00", 0),
        # rounded half up to whole rupiah
        ("Rp 35,636.36", 35636),
        ("Rp 3,563.64", 3564),
        ("12.50", 13),
        # no separator
        ("15000", 15000),
        ("909", 909),
        # noise around the number
        ("TOTAL 47,499", 47499),
        ("Rp 27.000", 27000),
        # negative: minus sign or accounting parentheses
        ("-300", -300),
        ("-36.900", -36900),
        ("39,800)", -39800),
        ("(0)", 0),
        # no digits at all
        ("-", None),
        ("", None),
    ],
)
def test_parse_amount(raw: str, expected: int | None) -> None:
    assert parse_amount(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "1.0000",  # 4 digits after the last separator
        "2 x 15,000",  # two numbers in one string: "15" is not a 3-digit group
        "1,00,000",  # middle group of 2 digits
    ],
)
def test_parse_amount_rejects_unknown_shapes(raw: str) -> None:
    with pytest.raises(ValueError, match="unrecognised amount format"):
        parse_amount(raw)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1", 1.0),
        ("11", 11.0),
        ("2X", 2.0),
        ("x1", 1.0),
        ("1 x", 1.0),
        ("1 X", 1.0),
        ("*2", 2.0),
        ("1.0", 1.0),
        ("1.00x", 1.0),
        ("1.00.", 1.0),  # stray trailing dot
        ("0.512X", 0.512),  # sold by weight: a separator in a count is a decimal point
        ("0.09X", 0.09),
        ("1,5", 1.5),
        ("x", None),
    ],
)
def test_parse_count(raw: str, expected: float | None) -> None:
    assert parse_count(raw) == expected


@pytest.mark.parametrize("raw", ["1 2", "1.000.5"])
def test_parse_count_rejects_unknown_shapes(raw: str) -> None:
    with pytest.raises(ValueError, match="unrecognised count format"):
        parse_count(raw)
