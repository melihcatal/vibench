
import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class DocumentExtractionRequest:
    """Represents a request for structured document extraction."""
    document_path: str
    extraction_config: Dict[str, Any] # Configuration for the extraction process

@dataclasses.dataclass
class ExtractedField:
    """Represents a single extracted field from a document."""
    field_name: str
    field_value: Any
    confidence: Optional[float] = None # Confidence score of the extraction

@dataclasses.dataclass
class DocumentExtractionResponse:
    """Represents the response from a structured document extraction."""
    document_path: str
    extracted_data: List[ExtractedField]
    status: str # e.g., "SUCCESS", "FAILED"
    error_message: Optional[str] = None

def normalize_extracted_data(response: DocumentExtractionResponse) -> Dict[str, Any]:
    """
    Normalizes the extracted data into a more consumable dictionary format.
    This is a basic example; real-world normalization might involve more complex logic
    like type conversion, data validation, or hierarchical structuring.
    """
    normalized_data = {}
    for field in response.extracted_data:
        normalized_data[field.field_name] = field.field_value
    return normalized_data

