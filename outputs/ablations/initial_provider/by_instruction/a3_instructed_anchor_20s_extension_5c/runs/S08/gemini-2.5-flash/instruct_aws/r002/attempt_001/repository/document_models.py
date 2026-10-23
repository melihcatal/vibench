from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class LineItemField:
    name: Optional[str] = None
    value: Optional[str] = None
    confidence: Optional[float] = None

@dataclass
class LineItem:
    fields: List[LineItemField] = field(default_factory=list)

@dataclass
class InvoiceDocument:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_textract_output: Optional[Dict[str, Any]] = None # To carry confidence scores etc.

@dataclass
class ReceiptDocument:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_textract_output: Optional[Dict[str, Any]] = None # To carry confidence scores etc.

@dataclass
class NormalizedExpense:
    document_type: str # "invoice" or "receipt"
    vendor_merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None # Applicable for receipts
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    original_extracted_data: Dict[str, Any] = field(default_factory=dict)
