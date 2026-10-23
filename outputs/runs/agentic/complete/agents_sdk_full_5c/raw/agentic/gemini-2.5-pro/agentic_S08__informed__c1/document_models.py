from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class InvoiceLineItem:
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    total_amount: Optional[float]

@dataclass
class Invoice:
    vendor_name: Optional[str]
    invoice_id: Optional[str]
    invoice_date: Optional[str]
    invoice_total: Optional[float]
    line_items: List[InvoiceLineItem] = field(default_factory=list)
    raw_response: Optional[Any] = None

@dataclass
class ReceiptLineItem:
    description: str
    quantity: float
    total_price: float

@dataclass
class Receipt:
    merchant_name: Optional[str]
    receipt_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    items: List[ReceiptLineItem] = field(default_factory=list)
    raw_response: Optional[Any] = None

@dataclass
class NormalizedExpenseLineItem:
    description: str
    amount: float

@dataclass
class NormalizedExpense:
    vendor: str
    transaction_date: str
    total: float
    line_items: List[NormalizedExpenseLineItem] = field(default_factory=list)
    category: Optional[str] = None
    source_document_id: Optional[str] = None
