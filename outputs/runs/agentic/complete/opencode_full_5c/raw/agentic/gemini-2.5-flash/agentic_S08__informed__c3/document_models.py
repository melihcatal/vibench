import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


@dataclasses.dataclass
class InvoiceExtractionResult:
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    total_amount: Optional[float] = None
    subtotal_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    invoice_id: Optional[str] = None
    purchase_order: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)
    raw_response: Dict[str, Any] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class ReceiptExtractionResult:
    merchant_name: Optional[str] = None
    merchant_address: Optional[str] = None
    transaction_date: Optional[str] = None
    transaction_time: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)
    raw_response: Dict[str, Any] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class NormalizedExpense:
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ValidationResult:
    is_valid: bool
    message: str
    issues: List[str] = dataclasses.field(default_factory=list)
