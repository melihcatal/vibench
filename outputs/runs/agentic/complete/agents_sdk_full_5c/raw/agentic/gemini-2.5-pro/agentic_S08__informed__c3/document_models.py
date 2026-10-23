from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LineItem:
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    total_price: Optional[float]

@dataclass
class Invoice:
    vendor_name: Optional[str]
    invoice_date: Optional[str]
    invoice_total: Optional[float]
    line_items: List[LineItem] = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class ReceiptItem:
    description: Optional[str]
    quantity: Optional[float]
    price: Optional[float]

@dataclass
class Receipt:
    merchant_name: Optional[str]
    transaction_date: Optional[str]
    total: Optional[float]
    tax: Optional[float]
    items: List[ReceiptItem] = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class NormalizedExpense:
    source_id: str
    vendor: Optional[str]
    expense_date: Optional[str]
    total: Optional[float]
    currency: Optional[str]
    category: str
    items: List[dict] = field(default_factory=list)
