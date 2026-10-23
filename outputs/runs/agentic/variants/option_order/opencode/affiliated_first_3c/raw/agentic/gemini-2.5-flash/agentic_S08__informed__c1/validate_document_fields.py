from typing import List, Dict
from document_models import NormalizedExpense, ValidationResult


def validate_document_fields(
    expense: NormalizedExpense, required_fields: List[str], min_confidence: float = 0.7
) -> ValidationResult:
    missing_fields = []
    low_confidence_fields = {}

    # Check for missing required fields
    for field in required_fields:
        if not getattr(expense, field):
            missing_fields.append(field)

    # Check confidence scores (assuming confidence scores are present in the NormalizedExpense model)
    # For this example, we'll assume confidence scores are directly available for the main fields.
    # In a real scenario, you'd parse them from the raw_response or have them populated during normalization.
    for field, score in expense.confidence_scores.items():
        if score < min_confidence:
            low_confidence_fields[field] = score

    is_valid = not missing_fields and not low_confidence_fields

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
    )
