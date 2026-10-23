from document_models import ExtractedExpense
from typing import Dict, Any

def validate_document_fields(expense: ExtractedExpense, required_fields: list[str]) -> Dict[str, Any]:
    """
    Validates required structured fields and provides a simple confidence score.

    Args:
        expense: The ExtractedExpense object to validate.
        required_fields: A list of field names that must be present (e.g., ["vendor_name", "total_amount"]).

    Returns:
        A dictionary with validation results, including a overall_confidence score.
    """
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "field_validation": {},
        "overall_confidence": 1.0 # Placeholder, as Textract analyze_expense doesn't give a single overall confidence
    }

    for field_name in required_fields:
        field_value = getattr(expense, field_name, None)
        if field_value is None:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field_name)
            validation_results["field_validation"][field_name] = {"present": False, "confidence": 0.0}
        else:
            validation_results["field_validation"][field_name] = {"present": True, "confidence": 1.0} # Assume 1.0 if present for now

    # A more sophisticated confidence could be derived from Textract's individual word confidences
    # For this simplified validation, if all required fields are present, confidence is high.
    if not validation_results["missing_fields"]:
        validation_results["overall_confidence"] = 0.95 # High confidence if all required fields found
    elif len(validation_results["missing_fields"]) < len(required_fields) / 2:
        validation_results["overall_confidence"] = 0.6 # Medium confidence if some missing
    else:
        validation_results["overall_confidence"] = 0.3 # Low confidence if many missing

    return validation_results
