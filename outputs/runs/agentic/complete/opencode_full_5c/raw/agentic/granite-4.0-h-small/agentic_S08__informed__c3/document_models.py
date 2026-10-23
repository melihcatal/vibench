# document_models.py
# Define request, response, and normalization helpers for Structured Document Extraction
from typing import TypedDict, List


class LineItem(TypedDict):
    description: str
    amount: float
    quantity: float
    unit: str | None


class ExpenseResponse(TypedDict):
    vendor_or_merchant: str
    date: str
    total: float
    currency: str
    tax: float | None
    line_items: List[LineItem]
    items: List[str] | None
