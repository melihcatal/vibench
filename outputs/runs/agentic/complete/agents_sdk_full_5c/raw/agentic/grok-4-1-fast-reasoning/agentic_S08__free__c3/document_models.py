from typing import TypedDict, List, Dict, Any, Optional, Union

class ExtractedField(TypedDict):
    value: Any
    confidence: float

class LineItem(TypedDict):
    description: str
    quantity: Optional[float]
    unit_price: float
    total_price: float

class InvoiceFields(TypedDict):
    vendor: ExtractedField
    date: ExtractedField
    total: ExtractedField
    line_items: List[LineItem]

class ReceiptFields(TypedDict):
    merchant: ExtractedField
    tax: ExtractedField
    total: ExtractedField
    items: List[LineItem]

class NormalizedExpense(TypedDict):
    expense_type: str
    vendor_or_merchant: str
    date: str
    subtotal: Optional[float]
    tax: Optional[float]
    total: float
    line_items: List[Dict[str, Any]]
    currency: str

class ValidationResult(TypedDict):
    is_valid: bool
    avg_confidence: float
    missing_fields: List[str]
    low_confidence_fields: List[str]