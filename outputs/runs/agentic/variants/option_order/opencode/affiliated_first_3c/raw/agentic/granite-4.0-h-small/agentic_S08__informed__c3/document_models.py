import json
from typing import TypedDict, List

### Normalized schema for expense documents
NormalizedExpense = TypedDict(
    "NormalizedExpense",
    {
        "vendor": str,
        "date": str,
        "total": float,
        "line_items": List["LineItem"],
    },
)

LineItem = TypedDict(
    "LineItem",
    {
        "description": str,
        "quantity": int,
        "unit_price": float,
        "total": float,
    },
)

### Example request payload for hosted LLM inference
InvoiceRequest = TypedDict(
    "InvoiceRequest",
    {
        "provider": str,
        "document": str,  # base64-encoded PDF or image
        "context": str,  # optional additional info
    },
)

### Example response from hosted LLM
InvoiceResponse = TypedDict(
    "InvoiceResponse",
    {
        "status": str,
        "data": NormalizedExpense,
        "confidence": float,
        "notes": str,
    },
)
