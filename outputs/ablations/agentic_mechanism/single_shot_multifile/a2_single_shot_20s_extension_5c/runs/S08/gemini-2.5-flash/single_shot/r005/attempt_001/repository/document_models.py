from typing import List, Dict, Any, Literal, TypedDict, Optional

class LineItem(TypedDict):
    description: str
    quantity: Optional[float]
    unit_price: Optional[float]
    amount: float

class InvoiceExtractionResult(TypedDict):
    vendor_name: Optional[str]
    invoice_date: Optional[str]
    invoice_total: Optional[float]
    line_items: List[LineItem]
    raw_data: Dict[str, Any]

class ReceiptExtractionResult(TypedDict):
    merchant_name: Optional[str]
    tax_amount: Optional[float]
    total_amount: Optional[float]
    items: List[LineItem]
    raw_data: str

class NormalizedExpense(TypedDict):
    id: str
    document_type: Literal['invoice', 'receipt']
    vendor_name: str
    transaction_date: str
    total_amount: float
    currency: str
    tax_amount: Optional[float]
    line_items: List[LineItem]
    notes: Optional[str]
    extracted_source: Dict[str, Any]

class ValidationResult(TypedDict):
    is_valid: bool
    reason: Optional[str]
    flags: List[str]
