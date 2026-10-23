import json
from typing import TypedDict, List, Literal

InvoiceLineItem = TypedDict("InvoiceLineItem", {"description": str, "amount": float})

InvoicePayload = TypedDict(
    "InvoicePayload",
    {"vendor": str, "date": str, "total": float, "line_items": List[InvoiceLineItem]},
)

ReceiptPayload = TypedDict(
    "ReceiptPayload",
    {
        "merchant": str,
        "date": str,
        "total": float,
        "line_items": List[InvoiceLineItem],  # use same typing for items
    },
)

NormalizedExpense = TypedDict(
    "NormalizedExpense",
    {
        "vendor": Literal[None],
        "merchant": str,
        "date": str,
        "total": float,
        "line_items": List[InvoiceLineItem],
    },
)
