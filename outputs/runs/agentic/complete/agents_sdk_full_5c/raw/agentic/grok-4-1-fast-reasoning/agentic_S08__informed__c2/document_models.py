from typing import TypedDict, List, Dict, Any, Optional

class ExtractedField(TypedDict):
    value: Any
    confidence: float

class LineItem(TypedDict):
    description: str
    quantity: Optional[float]
    price: float
    confidence: float

class InvoiceFields(TypedDict):
    vendor_name: ExtractedField
    invoice_date: ExtractedField
    total_amount: ExtractedField
    line_items: List[LineItem]

class ReceiptFields(TypedDict):
    merchant_name: ExtractedField
    transaction_date: ExtractedField
    total_amount: ExtractedField
    tax_amount: Optional[ExtractedField]
    line_items: List[LineItem]

class NormalizedExpense(TypedDict):
    doc_type: str
    merchant: str
    date: str
    total: float
    tax: Optional[float]
    items: List[Dict[str, Any]]
    avg_confidence: float