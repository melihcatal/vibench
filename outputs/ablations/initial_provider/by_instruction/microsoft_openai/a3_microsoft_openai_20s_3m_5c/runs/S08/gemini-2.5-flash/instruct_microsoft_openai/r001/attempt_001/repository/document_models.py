import dataclasses
from typing import List, Optional, Dict, Any

@dataclasses.dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    total_price: float

@dataclasses.dataclass
class InvoiceFields:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class ReceiptItem:
    description: str
    price: float

@dataclasses.dataclass
class ReceiptFields:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    items: List[ReceiptItem] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class NormalizedExpense:
    document_type: str # e.g., 'invoice', 'receipt'
    vendor_or_merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    # Additional fields can be added as needed

@dataclasses.dataclass
class FieldValidationResult:
    field_name: str
    is_valid: bool
    reason: Optional[str] = None

@dataclasses.dataclass
class DocumentValidationResult:
    is_valid: bool
    validation_details: List[FieldValidationResult] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class ContentModerationResult:
    is_safe: bool
    scores: Dict[str, float] = dataclasses.field(default_factory=dict)
