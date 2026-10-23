from document_models import NormalizedExpense, DocumentValidationResult
from typing import List

def validate_document_fields(
    expense: NormalizedExpense,
    required_fields: List[str],
    min_confidence_score: float = 0.7
) -> DocumentValidationResult:
    
    missing_fields = []
    low_confidence_fields = []

    for field in required_fields:
        if not hasattr(expense, field) or getattr(expense, field) is None:
            missing_fields.append(field)
    
    # Placeholder for confidence score validation, assuming confidence_score is a field in NormalizedExpense
    # and individual field confidences would be part of a more complex model.
    # For now, we'll just check the overall confidence if it exists.
    if expense.confidence_score is not None and expense.confidence_score < min_confidence_score:
        low_confidence_fields.append("overall_document_confidence")

    is_valid = not missing_fields and not low_confidence_fields
    
    return DocumentValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields
    )
