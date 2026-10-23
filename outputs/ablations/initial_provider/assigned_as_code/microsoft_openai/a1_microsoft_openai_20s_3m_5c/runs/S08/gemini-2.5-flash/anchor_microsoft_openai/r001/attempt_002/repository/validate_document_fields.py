from typing import Dict, Any, List
from document_models import NormalizedExpense, ValidationResult

def validate_document_fields(normalized_expense: NormalizedExpense, required_fields: List[str], min_confidence: float = 0.7) -> ValidationResult:
    missing_fields = []
    low_confidence_fields = {}

    # Check for required fields
    for field in required_fields:
        if not getattr(normalized_expense, field, None):
            missing_fields.append(field)

    # Check confidence scores (example: assume confidence_scores in NormalizedExpense contains field-level confidences)
    # For this example, we'll just check overall confidence if present, or assume 1.0 if not explicit.
    if normalized_expense.confidence_scores:
        for field, score in normalized_expense.confidence_scores.items():
            if score < min_confidence:
                low_confidence_fields[field] = score
    
    is_valid = not missing_fields and not low_confidence_fields
    message = "Document fields are valid." if is_valid else "Document fields are invalid."

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        message=message
    )
