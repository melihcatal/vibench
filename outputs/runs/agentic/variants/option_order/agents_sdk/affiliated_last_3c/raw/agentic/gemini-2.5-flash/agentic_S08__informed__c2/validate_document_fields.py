from document_models import NormalizedExpense
from typing import List, Tuple, Dict

def validate_document_fields(
    expense: NormalizedExpense,
    required_fields: List[str],
    min_confidence: float = 0.7
) -> Tuple[bool, Dict[str, str]]:
    """
    Validates required structured fields and their confidence scores in a NormalizedExpense.

    Args:
        expense: The NormalizedExpense object to validate.
        required_fields: A list of field names that must be present and meet confidence.
        min_confidence: The minimum confidence score required for a field to be considered valid.

    Returns:
        A tuple: (is_valid, validation_errors).
        is_valid: True if all required fields are present and meet confidence, False otherwise.
        validation_errors: A dictionary of field names to error messages for invalid fields.
    """
    is_valid = True
    validation_errors: Dict[str, str] = {}

    for field in required_fields:
        field_value = getattr(expense, field, None)
        confidence = expense.confidence_scores.get(field, 0.0)

        if field_value is None:
            is_valid = False
            validation_errors[field] = f"Required field '{field}' is missing."
        elif confidence < min_confidence:
            is_valid = False
            validation_errors[field] = f"Confidence for field '{field}' ({confidence:.2f}) is below minimum ({min_confidence:.2f})."

    # Additional validation for line items if needed
    if "line_items" in required_fields and not expense.line_items:
        is_valid = False
        validation_errors["line_items"] = "Required field 'line_items' is empty."
    elif "line_items" in required_fields and expense.line_items:
        for i, item in enumerate(expense.line_items):
            if not item.description or not item.amount: # Example: ensure description and amount are present for line items
                is_valid = False
                validation_errors[f"line_item_{i}"] = "Line item requires a description and amount."

    return is_valid, validation_errors
