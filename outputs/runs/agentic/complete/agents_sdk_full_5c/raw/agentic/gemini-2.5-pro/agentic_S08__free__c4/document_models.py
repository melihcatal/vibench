# document_models.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class InvoiceLineItem:
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    total_price: Optional[float]

@dataclass
class ExtractedInvoice:
    vendor_name: Optional[str]
    invoice_date: Optional[str]
    invoice_id: Optional[str]
    total_amount: Optional[float]
    line_items: List[InvoiceLineItem] = field(default_factory=list)
    raw_fields: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReceiptLineItem:
    description: Optional[str]
    quantity: Optional[float]
    price: Optional[float]

@dataclass
class ExtractedReceipt:
    merchant_name: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    items: List[ReceiptLineItem] = field(default_factory=list)
    raw_fields: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NormalizedExpense:
    vendor: str
    transaction_date: str
    total: float
    currency: str
    category: str
    line_items: List[Dict[str, Any]]
    source_document_type: str
    source_document_hash: str
