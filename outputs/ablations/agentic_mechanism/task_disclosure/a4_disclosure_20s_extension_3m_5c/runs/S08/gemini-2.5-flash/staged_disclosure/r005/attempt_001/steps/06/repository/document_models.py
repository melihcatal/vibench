import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class ExtractionRequest:
    document_id: str
    file_path: Optional[str] = None
    file_content: Optional[bytes] = None
    mime_type: Optional[str] = None
    extraction_config: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class ExtractionResponse:
    document_id: str
    status: str  # e.g., "SUCCESS", "FAILED", "PENDING"
    extracted_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time_ms: Optional[int] = None

def normalize_extracted_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes extracted data by performing common cleaning and standardization steps.
    This is a placeholder for actual normalization logic.
    """
    normalized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Example: Strip whitespace and convert to lowercase
            normalized_data[key] = value.strip()
        else:
            normalized_data[key] = value
    return normalized_data
