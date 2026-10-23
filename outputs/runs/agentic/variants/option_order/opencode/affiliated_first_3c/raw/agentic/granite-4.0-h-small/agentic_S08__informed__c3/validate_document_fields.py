import json


def validate_document_fields(data, required_fields):
    """Validates that required structured fields and confidence scores are present.
    Args:
        data (dict): Provider raw response data.
        required_fields (list): List of required field names (e.g., ['vendor','date','total','line_items']).
    Returns:
        bool: True if all required fields exist and have confidence >= 0.8, else False.
    """
    for field in required_fields:
        if field not in data or data[field]["confidence"] < 0.8:
            return False
    return True
