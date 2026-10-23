
import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class DocumentExtractionRequest:
    """
    Represents a request for structured document extraction.
    """
    document_content: bytes
    document_type: str  # e.g., "invoice", "receipt"
    extraction_params: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class DocumentExtractionResponse:
    """
    Represents the raw response from a structured document extraction service.
    """
    raw_response_data: Dict[str, Any]
    document_id: Optional[str] = None

@dataclasses.dataclass
class LineItem:
    """
    Represents a single line item in an expense document.
    """
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None

@dataclasses.dataclass
class NormalizedExpenseDocument:
    """
    Represents a normalized expense document with common fields.
    """
    document_type: str  # e.g., "invoice", "receipt"
    vendor_name: Optional[str] = None
    document_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    merchant_name: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)
    notes: Optional[str] = None
    raw_extraction_data: Optional[Dict[str, Any]] = None
