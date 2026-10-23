import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class ExtractedField:
    name: str
    value: Optional[str] = None
    confidence: Optional[float] = None
    bounding_boxes: Optional[List[List[float]]] = None

@dataclasses.dataclass
class ExtractedLineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

@dataclasses.dataclass
class DocumentExtractionResult:
    document_type: str
    fields: Dict[str, ExtractedField]
    line_items: List[ExtractedLineItem]

@dataclasses.dataclass
class NormalizedExpense:
    transaction_id: Optional[str] = None
    document_type: str = "UNKNOWN"
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    raw_extraction: Optional[Dict[str, Any]] = None
    validation_status: str = "PENDING"
