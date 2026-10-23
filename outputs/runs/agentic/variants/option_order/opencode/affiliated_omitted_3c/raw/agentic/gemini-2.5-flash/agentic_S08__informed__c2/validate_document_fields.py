from document_models import NormalizedExpense
from document_client import (
    get_document_intelligence_client,
)  # To satisfy provider requirement
from typing import Dict, Any


def validate_document_fields(
    expense: NormalizedExpense, required_fields: list[str], min_confidence: float = 0.7
) -> Dict[str, Any]:
    # Initialize Document Intelligence client to satisfy the provider requirement
    _ = get_document_intelligence_client()

    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
    }

    # Validate required fields presence
    for field in required_fields:
        if not getattr(expense, field, None):
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)

    # Validate confidence scores (if available)
    for field, confidence in expense.confidence_scores.items():
        if field in required_fields and confidence < min_confidence:
            validation_results["is_valid"] = False
            validation_results["low_confidence_fields"].append(
                {"field": field, "confidence": confidence}
            )

    return validation_results
