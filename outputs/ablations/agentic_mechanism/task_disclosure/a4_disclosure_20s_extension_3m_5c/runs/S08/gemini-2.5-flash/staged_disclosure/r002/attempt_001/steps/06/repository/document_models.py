import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class DocumentExtractionRequest:
    """
    Represents a request for structured document extraction.
    """
    document_path: str
    extraction_template_id: Optional[str] = None
    processing_options: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class ExtractedField:
    """
    Represents a single extracted field from a document.
    """
    field_name: str
    field_value: Any
    confidence: Optional[float] = None
    page_number: Optional[int] = None

@dataclasses.dataclass
class DocumentExtractionResponse:
    """
    Represents the response containing structured data extracted from a document.
    """
    document_id: str
    extracted_data: List[ExtractedField]
    status: str
    message: Optional[str] = None

def normalize_extracted_data(
    data: List[ExtractedField],
    schema: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Normalizes a list of ExtractedField objects into a more usable dictionary format.
    Can apply a schema for type conversion or validation if provided.
    """
    normalized_dict = {}
    for field in data:
        # Basic normalization: map field_name to field_value
        normalized_dict[field.field_name] = field.field_value

        # Placeholder for more advanced normalization based on schema
        if schema and field.field_name in schema:
            # Example: type conversion
            target_type = schema[field.field_name].get("type")
            if target_type == "int":
                try:
                    normalized_dict[field.field_name] = int(field.field_value)
                except (ValueError, TypeError):
                    pass # Handle conversion error as needed
            elif target_type == "float":
                try:
                    normalized_dict[field.field_name] = float(field.field_value)
                except (ValueError, TypeError):
                    pass # Handle conversion error as needed
            # Add more type conversions or validation logic here

    return normalized_dict
