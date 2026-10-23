from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    total: float

@dataclass
class InvoiceFields:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)

@dataclass
class ReceiptFields:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    items: List[LineItem] = field(default_factory=list)

@dataclass
class NormalizedExpense:
    document_type: str # e.g., "invoice", "receipt"
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_document_text: Optional[str] = None

@dataclass
class ValidationResult:
    field_name: str
    is_valid: bool
    confidence: float
    message: Optional[str] = None
