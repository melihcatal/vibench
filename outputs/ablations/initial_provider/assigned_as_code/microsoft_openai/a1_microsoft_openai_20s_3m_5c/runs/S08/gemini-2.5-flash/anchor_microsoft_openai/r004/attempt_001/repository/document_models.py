from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DocumentField:
    content: Optional[str] = None
    confidence: Optional[float] = None

@dataclass
class LineItem:
    description: Optional[DocumentField] = None
    quantity: Optional[DocumentField] = None
    amount: Optional[DocumentField] = None

@dataclass
class InvoiceExtraction:
    vendor: Optional[DocumentField] = None
    date: Optional[DocumentField] = None
    total: Optional[DocumentField] = None
    line_items: List[LineItem] = field(default_factory=list)

@dataclass
class ReceiptExtraction:
    merchant: Optional[DocumentField] = None
    tax: Optional[DocumentField] = None
    total: Optional[DocumentField] = None
    items: List[LineItem] = field(default_factory=list)

@dataclass
class NormalizedExpense:
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    raw_extraction_data: Dict[str, Any] = field(default_factory=dict)
