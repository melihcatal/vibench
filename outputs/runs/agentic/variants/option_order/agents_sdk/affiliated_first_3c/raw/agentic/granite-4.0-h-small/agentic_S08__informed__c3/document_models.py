from typing import TypedDict, List

class InvoicePayload(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: List[dict]  # each item can have description, quantity, price
    confidence: float

class ReceiptPayload(TypedDict):
    merchant: str
    tax: float
    total: float
    items: List[dict]  # each item can have name, quantity, price
    confidence: float

class NormalizedExpense(TypedDict):
    vendor_or_merchant: str
    date: str
    total: float
    line_items_or_items: List[dict]
    confidence: float