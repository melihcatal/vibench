"""
Local request, response, and normalization helpers for Structured Document Extraction.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class LineItem:
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    total_amount: Optional[float]

@dataclass
class Invoice:
    vendor_name: Optional[str]
    invoice_date: Optional[str]
    invoice_total: Optional[float]
    items: List[LineItem] = field(default_factory=list)

@dataclass
class Receipt:
    merchant_name: Optional[str]
    transaction_date: Optional[str]
    tax: Optional[float]
    total: Optional[float]
    items: List[LineItem] = field(default_factory=list)


@dataclass
class NormalizedExpense:
    expense_id: str
    vendor: str
    transaction_date: str
    total_amount: float
    currency: str
    category: Optional[str] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    source_document_url: Optional[str] = None
    raw_extraction_data: Dict[str, Any] = field(default_factory=dict)
