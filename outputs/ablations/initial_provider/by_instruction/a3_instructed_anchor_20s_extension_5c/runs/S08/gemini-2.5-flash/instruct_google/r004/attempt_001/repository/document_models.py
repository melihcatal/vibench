from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

@dataclass
class Invoice:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)

@dataclass
class Receipt:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    items: List[LineItem] = field(default_factory=list)

@dataclass
class DocumentValidationResult:
    field_name: str
    is_valid: bool
    confidence: float
    message: Optional[str] = None
