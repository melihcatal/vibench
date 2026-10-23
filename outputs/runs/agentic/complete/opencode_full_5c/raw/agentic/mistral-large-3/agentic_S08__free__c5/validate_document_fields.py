from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, validator


class ValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Whether the document fields are valid")
    missing_fields: List[str] = Field(
        default_factory=list, description="List of missing required fields"
    )
    low_confidence_fields: Dict[str, float] = Field(
        default_factory=dict, description="Fields with low confidence scores"
    )
    errors: List[str] = Field(
        default_factory=list, description="List of validation errors"
    )


def validate_document_fields(
    extracted_data: Dict[str, Any],
    required_fields: Optional[List[str]] = None,
    confidence_threshold: float = 0.8,
) -> ValidationResult:
    """
    Validates required structured fields and confidence scores using Pydantic and custom rules.
    """
    if required_fields is None:
        required_fields = ["vendor", "date", "total"]

    result = ValidationResult(is_valid=True)

    # Check for missing required fields
    for field in required_fields:
        if field not in extracted_data or extracted_data[field] is None:
            result.is_valid = False
            result.missing_fields.append(field)

    # Check confidence scores
    if (
        "confidence" in extracted_data
        and extracted_data["confidence"] < confidence_threshold
    ):
        result.is_valid = False
        result.low_confidence_fields["overall"] = extracted_data["confidence"]

    # Field-specific confidence checks (if available)
    for field in required_fields:
        if (
            f"{field}_confidence" in extracted_data
            and extracted_data[f"{field}_confidence"] < confidence_threshold
        ):
            result.is_valid = False
            result.low_confidence_fields[field] = extracted_data[f"{field}_confidence"]

    # Validate date format if present
    if "date" in extracted_data and extracted_data["date"]:
        try:
            from datetime import datetime

            if not isinstance(extracted_data["date"], datetime):
                datetime.fromisoformat(extracted_data["date"])
        except (ValueError, TypeError):
            result.is_valid = False
            result.errors.append(
                f"Invalid date format for field 'date': {extracted_data['date']}"
            )

    # Validate numeric fields if present
    for field in ["total", "tax"]:
        if field in extracted_data and extracted_data[field] is not None:
            try:
                float(extracted_data[field])
            except (ValueError, TypeError):
                result.is_valid = False
                result.errors.append(
                    f"Invalid numeric value for field '{field}': {extracted_data[field]}"
                )

    return result
