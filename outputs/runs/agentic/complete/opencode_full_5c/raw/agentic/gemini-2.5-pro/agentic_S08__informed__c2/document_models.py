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
    vendor_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    invoice_id: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    total_amount: Optional[float] = None
    total_tax: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_document: Optional[dict] = None


@dataclass
class Receipt:
    merchant_name: Optional[str] = None
    merchant_address: Optional[str] = None
    transaction_date: Optional[str] = None
    transaction_time: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    items: List[LineItem] = field(default_factory=list)
    raw_document: Optional[dict] = None


@dataclass
class Expense:
    vendor: str
    date: str
    total: float
    line_items: List[LineItem]
    source_document_type: str
