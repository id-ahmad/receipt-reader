"""The target schema (ADR 0001, ADR 0002): what every system outputs and is scored against.

Every field is required but may be null, so "not on the receipt" is always stated
explicitly. The descriptions are the field definitions; they will also go to the models.
"""

from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Item name as printed on the receipt.")
    count: float | None = Field(
        description="Quantity bought. Usually a whole number; a decimal for items sold by "
        "weight (e.g. 0.512). Null if not printed."
    )
    price: int | None = Field(
        description="What this line costs in whole rupiah (count × unit price), not the "
        "unit price. Null if not printed."
    )


class Receipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[Item] = Field(description="Every item bought, in receipt order.")
    subtotal: int | None = Field(
        description="Sum of the items before tax, service and discount, in whole rupiah. "
        "Some receipts print this line as 'TOTAL'. Null if not printed."
    )
    tax: int | None = Field(description="Tax charged, in whole rupiah. Null if none.")
    service: int | None = Field(description="Service charge, in whole rupiah. Null if none.")
    discount: int | None = Field(
        description="Total discount as a positive number of whole rupiah. Null if none."
    )
    total: int | None = Field(
        description="Final amount the customer owes, after tax, service and discount, in "
        "whole rupiah. Often printed as 'GRAND TOTAL', not necessarily the line that says "
        "'TOTAL'. Null if not printed."
    )
