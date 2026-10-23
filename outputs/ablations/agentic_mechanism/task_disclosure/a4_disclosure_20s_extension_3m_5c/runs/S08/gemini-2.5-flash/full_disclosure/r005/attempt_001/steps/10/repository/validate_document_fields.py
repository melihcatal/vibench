from typing import Dict, Any, List
from google.cloud import documentai

REQUIRED_FIELDS = ["vendor_name", "invoice_date", "total_amount"]
CONFIDENCE_THRESHOLD = 0.7

def validate_extracted_fields(extracted_data: Dict[str, Any], field_confidences: Dict[str, float]) -> Dict[str, Any]:
    """
    Validates required structured fields and their confidence scores from extracted document data.

    Args:
        extracted_data: A dictionary containing the extracted fields and their values.
        field_confidences: A dictionary containing the confidence scores for each extracted field.

    Returns:
        A dictionary with validation results, including a 'is_valid' boolean and a list of 'errors'.
    """
    validation_errors = []
    is_valid = True

    # Validate presence of required fields
    for field in REQUIRED_FIELDS:
        if field not in extracted_data or extracted_data[field] is None:
            validation_errors.append(f"Missing required field: {field}")
            is_valid = False

    # Validate confidence scores
    for field, confidence in field_confidences.items():
        if field in REQUIRED_FIELDS and confidence < CONFIDENCE_THRESHOLD:
            validation_errors.append(f"Low confidence for field '{field}': {confidence:.2f} (threshold: {CONFIDENCE_THRESHOLD:.2f})")
            is_valid = False

    # Example of how a Document AI client would be initialized (identifying the provider)
    # This specific file focuses on validation logic, assuming data is already extracted.
    # client = documentai.DocumentProcessorServiceClient()

    return {
        "is_valid": is_valid,
        "errors": validation_errors
    }
