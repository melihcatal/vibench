"""
validate_document_fields.py

Validates required structured fields and confidence scores from an Expense object.
"""

from typing import List, Dict, Any
from document_models import Expense

def validate_expense_fields(expense: Expense, required_fields: List[str]) -> Dict[str, Any]:
    """
    Validates that all required fields are present and not None in an Expense object.

    Args:
        expense: The Expense object to validate.
        required_fields: A list of string names of fields that must be present (e.g., ['vendor_name', 'total_amount']).

    Returns:
        A dictionary with validation results, including a boolean 'is_valid' and a list of 'missing_fields'.
    """
    missing_fields = []
    is_valid = True

    for field in required_fields:
        if not hasattr(expense, field) or getattr(expense, field) is None:
            missing_fields.append(field)
            is_valid = False
    
    # Example of additional validation logic for specific types
    if 'total_amount' in required_fields and expense.total_amount is not None and expense.total_amount <= 0:
        is_valid = False
        if "total_amount" not in missing_fields:
            missing_fields.append("total_amount_invalid_value")

    return {
        "is_valid": is_valid,
        "missing_fields": missing_fields,
        "validation_details": f"Expense validation: {len(missing_fields)} missing/invalid fields detected."
    }

def check_field_confidence(
    field_value: Any,
    confidence_score: float,
    min_confidence: float = 0.8
) -> bool:
    """
    Checks if a field's extracted confidence score meets a minimum threshold.
    (Placeholder - actual confidence scores would come from the Document AI output structure).

    Args:
        field_value: The value of the extracted field.
        confidence_score: The confidence score associated with the extraction.
        min_confidence: The minimum acceptable confidence score.

    Returns:
        True if confidence meets the threshold, False otherwise.
    """
    # In a real scenario, confidence would be part of the extracted_fields dict
    # For this example, we assume `confidence_score` is directly passed.
    return confidence_score >= min_confidence
