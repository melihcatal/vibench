from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class LineItem:
    description: Optional[str] = None
    amount: Optional[float] = None
    quantity: Optional[float] = None


@dataclass
class NormalizedExpense:
    vendor_name: str
    transaction_date: str
    total_amount: float
    currency: str = "USD"
    line_items: List[LineItem] = field(default_factory=list)
    category: Optional[str] = None
    notes: Optional[str] = None
    source_document_type: Optional[str] = None  # e.g., "Invoice", "Receipt"


@dataclass
class InvoiceFields:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_total: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
    note: Optional[str] = None


@dataclass
class ReceiptFields:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    items: List[LineItem] = field(default_factory=list)
    note: Optional[str] = None
