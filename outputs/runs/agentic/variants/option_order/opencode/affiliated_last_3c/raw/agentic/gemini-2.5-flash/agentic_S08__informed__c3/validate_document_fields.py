from document_models import NormalizedExpense
from typing import List, Tuple


def validate_document_fields(
    expense: NormalizedExpense, required_fields: List[str], min_confidence: float = 0.7
) -> Tuple[bool, List[str]]:
    missing_fields = []
    for field in required_fields:
        if getattr(expense, field) is None:
            missing_fields.append(field)

    # In a real scenario, confidence scores would be part of the NormalizedExpense model from the raw_extraction
    # For this example, we'll just check for missing fields.

    is_valid = len(missing_fields) == 0
    return is_valid, missing_fields
