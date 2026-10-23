from typing import TypedDict, List, Dict, Any, Optional

class ExtractedField(TypedDict):
    content: str
    confidence: float

class LineItem(TypedDict):
    description: str
    quantity: Optional[float]
    price: Optional[float]
    amount: float

class InvoiceExtract(TypedDict):
    vendor: ExtractedField
    date: ExtractedField
    total: ExtractedField
    line_items: List[LineItem]

class ReceiptExtract(TypedDict):
    merchant: ExtractedField
    date: ExtractedField
    tax: Optional[ExtractedField]
    total: ExtractedField
    items: List[LineItem]

class NormalizedExpense(TypedDict):
    type: str
    vendor_or_merchant: str
    date: str
    total: float
    tax: Optional[float]
    line_items: List[LineItem]
