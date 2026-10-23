import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

@dataclasses.dataclass
class Invoice:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class Receipt:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    items: List[LineItem] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class NormalizedExpense:
    document_type: str # 'invoice' or 'receipt'
    provider: str # e.g., 'google_document_ai'
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)
    raw_extraction: dict = dataclasses.field(default_factory=dict)
