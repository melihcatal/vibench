import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class DocumentExtractionRequest:
    """Represents a request for structured document extraction."""
    document_content: str
    document_type: str
    extraction_template_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class ExtractedField:
    """Represents a single extracted field from a document."""
    field_name: str
    field_value: Any
    confidence: Optional[float] = None
    page_number: Optional[int] = None

@dataclasses.dataclass
class DocumentExtractionResponse:
    """Represents the response from a structured document extraction."""
    document_id: str
    extracted_data: List[ExtractedField]
    status: str
    processing_time_ms: Optional[int] = None
    error_message: Optional[str] = None

def normalize_document_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes extracted document data.

    This is a placeholder for actual normalization logic, which might include:
    - Type conversion (e.g., string to int/float/date)
    - Data cleaning (e.g., removing extra whitespace, standardizing formats)
    - Mapping field names
    - Handling missing values

    Args:
        data: A dictionary containing the raw extracted data.

    Returns:
        A dictionary with the normalized data.
    """
    # Example: Simple normalization (e.g., stripping whitespace from string values)
    normalized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            normalized_data[key] = value.strip()
        else:
            normalized_data[key] = value
    return normalized_data
