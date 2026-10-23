from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class ValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Whether the document fields are valid")
    missing_fields: list[str] = Field(
        default_factory=list, description="List of missing required fields"
    )
    confidence_score: Optional[float] = Field(
        default=None, description="Confidence score of the extraction"
    )
    confidence_valid: bool = Field(
        default=False, description="Whether the confidence score meets the threshold"
    )


def validate_document_fields(
    extracted_data: Dict[str, Any],
    document_type: str,
    confidence_threshold: float = 0.7,
) -> ValidationResult:
    required_fields = {
        "invoice": ["vendor", "date", "total", "line_items"],
        "receipt": ["merchant", "total", "items"],
    }

    if document_type not in required_fields:
        raise ValueError(f"Unsupported document type: {document_type}")

    missing_fields = []
    for field in required_fields[document_type]:
        if field not in extracted_data or extracted_data[field] is None:
            missing_fields.append(field)
        elif field in ["line_items", "items"] and len(extracted_data[field]) == 0:
            missing_fields.append(field)

    confidence = extracted_data.get("confidence", 0.0)
    confidence_valid = confidence >= confidence_threshold

    return ValidationResult(
        is_valid=len(missing_fields) == 0 and confidence_valid,
        missing_fields=missing_fields,
        confidence_score=confidence,
        confidence_valid=confidence_valid,
    )
