from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


@dataclass
class ExtractedInvoiceFields:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class ExtractedReceiptFields:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class NormalizedExpense:
    document_type: str  # e.g., 'invoice', 'receipt'
    vendor_or_merchant_name: str
    transaction_date: str
    total_amount: float
    currency: str = "USD"
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_extraction_confidence: float = 0.0
    notes: Optional[str] = None


@dataclass
class ValidationResult:
    is_valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
    message: str = ""
