from typing import TypedDict, List, Any

class InvoiceModel(TypedDict):
    vendor: str
    date: str
    total: float
    currency: str
    line_items: List[dict]

class ReceiptModel(TypedDict):
    merchant: str
    items: List[dict]
    subtotal: float
    tax: float
    total: float

class NormalizedExpense(TypedDict):
    vendor: str
    amount: float
    currency: str
    date: str
    line_items: List[dict]
    metadata: Any
