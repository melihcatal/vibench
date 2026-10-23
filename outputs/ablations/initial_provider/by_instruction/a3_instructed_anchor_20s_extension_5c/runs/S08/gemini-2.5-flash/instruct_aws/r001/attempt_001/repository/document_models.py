from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[str] = None
    unit_price: Optional[str] = None
    total: Optional[str] = None

@dataclass
class ExtractedDocument:
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[str] = None
    currency: Optional[str] = None
    tax_amount: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_extraction: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DocumentValidationResult:
    is_valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
