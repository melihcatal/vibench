# validate_document_fields.py
# Validate required structured fields and confidence scores from document extraction
import json


def validate_fields(normalized_fields):
    """Check that mandatory fields are present and have sufficient confidence.

    Args:
        normalized_fields (dict): Normalized expense data.
    Returns:
        bool: True if validation passes, False otherwise.
    """
    required = ["vendor_or_merchant", "date", "total", "currency"]
    missing = [f for f in required if not normalized_fields.get(f)]
    if missing:
        print(f"Validation error: missing required fields {missing}")
        return False
    # Example confidence check (assuming provider adds a 'confidence' key at field level)
    for key, value in normalized_fields.items():
        if (
            isinstance(value, dict)
            and "confidence" in value
            and value["confidence"] < 0.8
        ):
            print(f"Low confidence for field {key}: {value['confidence']}")
            return False
    return True
