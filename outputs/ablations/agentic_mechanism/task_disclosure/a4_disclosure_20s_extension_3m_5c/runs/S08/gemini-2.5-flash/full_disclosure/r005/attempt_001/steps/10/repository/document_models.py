from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class DocumentExtractionRequest:
    document_content: str  # Base64 encoded document content (e.g., image, PDF)
    document_type: Optional[str] = None # e.g., "invoice", "receipt"

@dataclass
class ExtractionField:
    name: str
    value: Any
    confidence: Optional[float] = None
    text_content: Optional[str] = None # Original text content from which the value was extracted

@dataclass
class DocumentExtractionResponse:
    fields: List[ExtractionField] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None # Store the raw response from an external API if any

@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None

@dataclass
class NormalizedExpense:
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None # ISO 8601 format YYYY-MM-DD
    total_amount: Optional[float] = None
    currency: Optional[str] = None # ISO 4217 format (e.g., "USD")
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
    document_type: Optional[str] = None # e.g., "invoice", "receipt"
    notes: Optional[str] = None
    original_document_id: Optional[str] = None
