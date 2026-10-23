from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import datetime

@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None

@dataclass
class Invoice:
    vendor_name: Optional[str] = None
    invoice_date: Optional[datetime.date] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_document_url: Optional[str] = None
    document_id: Optional[str] = None

@dataclass
class Receipt:
    merchant_name: Optional[str] = None
    transaction_date: Optional[datetime.date] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    items: List[LineItem] = field(default_factory=list)
    raw_document_url: Optional[str] = None
    document_id: Optional[str] = None

@dataclass
class NormalizedExpenseItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None # Standardized currency

@dataclass
class NormalizedExpense:
    source_document_type: str # "invoice" or "receipt"
    primary_vendor_merchant: Optional[str] = None
    transaction_date: Optional[datetime.date] = None
    total_expense_amount: Optional[float] = None
    total_tax_amount: Optional[float] = None
    standardized_currency: str = "USD" # Default to USD after conversion
    expense_items: List[NormalizedExpenseItem] = field(default_factory=list)
    source_document_id: Optional[str] = None
    notes: Optional[str] = None # For vendor notes, etc.
    validation_status: Dict[str, Any] = field(default_factory=dict)
