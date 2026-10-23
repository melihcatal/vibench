from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field, validator


class ValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Whether the document fields are valid")
    missing_fields: list[str] = Field(
        default_factory=list, description="List of missing required fields"
    )
    confidence_score: float = Field(
        ..., description="Confidence score of the validation"
    )
    errors: list[str] = Field(
        default_factory=list, description="List of validation errors"
    )


def validate_document_fields(
    extracted_data: Dict[str, Any], min_confidence: float = 0.7
) -> ValidationResult:
    """
    Validates required structured fields and confidence scores for extracted document data.
    """
    required_fields = {
        "vendor": "vendor" in extracted_data,
        "date": "date" in extracted_data,
        "total": "total" in extracted_data,
    }

    missing_fields = [
        field for field, present in required_fields.items() if not present
    ]
    confidence = extracted_data.get("confidence", 0.0)
    is_valid = not missing_fields and confidence >= min_confidence
    errors = []

    if confidence < min_confidence:
        errors.append(
            f"Confidence score {confidence} is below the minimum threshold {min_confidence}"
        )

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        confidence_score=confidence,
        errors=errors,
    )
