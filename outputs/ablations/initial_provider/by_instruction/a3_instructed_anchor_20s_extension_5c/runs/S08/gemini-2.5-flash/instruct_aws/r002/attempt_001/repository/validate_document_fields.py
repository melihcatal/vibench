from typing import List
from document_models import NormalizedExpense

def validate_document_fields(expense: NormalizedExpense, required_fields: List[str], min_confidence: float = 0.8) -> Dict[str, Any]:
    """Validates required structured fields and confidence scores of a NormalizedExpense.

    Args:
        expense: A NormalizedExpense object.
        required_fields: A list of field names that must be present (e.g., ['vendor_merchant_name', 'total_amount'])
        min_confidence: Minimum required confidence score for fields.

    Returns:
        A dictionary with validation results, including missing fields and low confidence fields.
    """
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": []
    }

    # Validate required fields presence
    for field in required_fields:
        if not getattr(expense, field, None):
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)

    # Validate confidence scores
    for field_name, confidence in expense.confidence_scores.items():
        if confidence < min_confidence:
            validation_results["is_valid"] = False
            validation_results["low_confidence_fields"].append({
                "field": field_name,
                "confidence": confidence
            })

    return validation_results
