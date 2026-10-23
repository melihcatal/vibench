import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

@dataclasses.dataclass
class ExtractedInvoiceFields:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class ExtractedReceiptFields:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class NormalizedExpense:
    document_type: str # "invoice" or "receipt"
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)
    raw_extraction: dict = dataclasses.field(default_factory=dict) # To store raw provider response

@dataclasses.dataclass
class DocumentFieldValidation:
    field_name: str
    is_present: bool
    confidence: float
    expected_type: str
    actual_value: Optional[str] = None
    is_valid: bool = False
    validation_message: Optional[str] = None
