from typing import Any

import pytest

from receipt_reader.cord import apply_corrections, convert_ground_truth
from receipt_reader.schema import Item, Receipt

A_FUNG: dict[str, Any] = {
    "menu": [
        {"nm": "BASO KUAH", "unitprice": "43,636", "cnt": "1", "price": "43,636"},
        {"nm": "NASI PUTIH", "unitprice": "6.000", "cnt": "1", "price": "6.000"},
        {"nm": "A.MINERAL BOTOL", "unitprice": "8,000", "cnt": "1", "price": "8,000"},
    ],
    "sub_total": {"subtotal_price": "57,636", "tax_price": "5,764"},
    "total": {"total_price": "63,400", "cashprice": "70.000", "changeprice": "6.600"},
}


def test_converts_the_a_fung_receipt() -> None:
    assert convert_ground_truth(A_FUNG) == Receipt(
        items=[
            Item(name="BASO KUAH", count=1, price=43636),
            Item(name="NASI PUTIH", count=1, price=6000),
            Item(name="A.MINERAL BOTOL", count=1, price=8000),
        ],
        subtotal=57636,
        tax=5764,
        service=None,
        discount=None,
        total=63400,
    )


def test_single_item_menu_is_an_object_not_a_list() -> None:
    receipt = convert_ground_truth(
        {"menu": {"nm": "KOPI", "cnt": "2X", "price": "30.000"}, "total": {"total_price": "30.000"}}
    )
    assert receipt.items == [Item(name="KOPI", count=2, price=30000)]


def test_discount_is_stored_positive_whatever_its_sign() -> None:
    for raw in ["-36.900", "36.900)", "(36.900)", "36.900"]:
        receipt = convert_ground_truth({"menu": [], "sub_total": {"discount_price": raw}})
        assert receipt.discount == 36900


def test_several_tax_lines_are_added_up() -> None:
    receipt = convert_ground_truth({"menu": [], "sub_total": {"tax_price": ["1.000", "2.500"]}})
    assert receipt.tax == 3500


def test_missing_sections_and_dash_become_null() -> None:
    receipt = convert_ground_truth({"menu": [], "sub_total": {"tax_price": "-"}})
    assert (receipt.subtotal, receipt.tax, receipt.total) == (None, None, None)


def test_item_with_no_name_is_kept_with_an_empty_name() -> None:
    receipt = convert_ground_truth({"menu": [{"cnt": "3", "price": "36.000"}]})
    assert receipt.items == [Item(name="", count=3, price=36000)]


def test_item_name_in_several_pieces_is_joined() -> None:
    receipt = convert_ground_truth({"menu": [{"nm": ["TAKEOUT(1):", "Viet Latte"]}]})
    assert receipt.items[0].name == "TAKEOUT(1): Viet Latte"


def test_several_sub_total_blocks_are_merged_first_value_wins() -> None:
    receipt = convert_ground_truth(
        {
            "menu": [],
            "sub_total": [
                {"subtotal_price": "18,182", "discount_price": "-2.727", "tax_price": "1,546"},
                {"subtotal_price": "15,455"},
            ],
        }
    )
    assert (receipt.subtotal, receipt.discount, receipt.tax) == (18182, 2727, 1546)


def test_item_name_of_unknown_type_is_rejected() -> None:
    with pytest.raises(TypeError, match="item name"):
        convert_ground_truth({"menu": [{"nm": 42, "price": "1.000"}]})


FIX = {
    "split": "train",
    "index": 7,
    "path": ["total", "total_price"],
    "raw": "385,0000",
    "fixed": "385,000",
    "reason": "typo",
}


def test_correction_replaces_the_raw_label() -> None:
    parse = apply_corrections("train", 7, {"total": {"total_price": "385,0000"}}, [FIX])
    assert parse["total"]["total_price"] == "385,000"


def test_correction_only_applies_to_its_own_receipt() -> None:
    parse = apply_corrections("train", 8, {"total": {"total_price": "1.000"}}, [FIX])
    assert parse["total"]["total_price"] == "1.000"


def test_correction_fails_loudly_if_the_raw_label_changed() -> None:
    with pytest.raises(ValueError, match="expected '385,0000'"):
        apply_corrections("train", 7, {"total": {"total_price": "999"}}, [FIX])
