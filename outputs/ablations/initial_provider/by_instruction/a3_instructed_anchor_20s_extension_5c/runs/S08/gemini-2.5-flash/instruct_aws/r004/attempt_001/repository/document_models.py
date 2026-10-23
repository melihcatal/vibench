import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class ExtractedInvoice:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[Dict[str, Any]] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class ExtractedReceipt:
    merchant_name: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    items: List[Dict[str, Any]] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class NormalizedExpense:
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    raw_extraction_data: Dict[str, Any] = dataclasses.field(default_factory=dict)
