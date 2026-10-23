
import dataclasses
from typing import List, Any, Optional

@dataclasses.dataclass
class DocumentExtractionRequest:
    """Represents a request for structured document extraction."""
    document_path: str
    document_type: str
    extraction_profile: Optional[str] = None

@dataclasses.dataclass
class ExtractionField:
    """Represents a single extracted field from a document."""
    name: str
    value: Any
    confidence: float
    page_number: Optional[int] = None
    bounding_box: Optional[List[float]] = None # [x1, y1, x2, y2]

@dataclasses.dataclass
class DocumentExtractionResponse:
    """Represents the response containing structured fields extracted from a document."""
    fields: List[ExtractionField]
    document_id: Optional[str] = None
    status: str = "success"
    message: Optional[str] = None

def normalize_fields(extracted_fields: List[ExtractionField]) -> dict:
    """
    Normalizes a list of ExtractionField objects into a flat dictionary.
    This is a basic normalization; more complex logic might be needed for real-world scenarios.
    """
    normalized_data = {}
    for field in extracted_fields:
        normalized_data[field.name] = field.value
    return normalized_data

