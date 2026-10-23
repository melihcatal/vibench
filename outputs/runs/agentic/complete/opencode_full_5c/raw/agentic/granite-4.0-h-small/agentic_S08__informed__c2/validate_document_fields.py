# [SAME-SCENARIO] validate_document_fields.py

# Validates extracted fields and confidence scores from SDK responses

from typing import Dict, Any, List


def validate_document_fields(raw_response: Dict[str, Any]) -> bool:
    """Validate that required structured fields exist and confidence scores are above thresholds.

    Args:
        raw_response: The raw dict returned by the SDK processor (e.g., Document AI).
    Returns:
        True if all required fields are present and confidence >= 0.9, else False.
    """
    # Example placeholders for field paths - adjust to actual SDK structure
    confidence_threshold = 0.9

    # Helper to check confidence
    def check_confidence(value: Any) -> bool:
        # Assuming value has a 'confidence' key between 0 and 1
        return isinstance(value, dict) and 0 <= value.get("confidence", 0) <= 1

    # Check invoice fields
    if not check_confidence(raw_response.get("vendor")):
        return False
    if not check_confidence(raw_response.get("invoice_date")):
        return False
    if not check_confidence(raw_response.get("total_amount")):
        return False
    items = raw_response.get("line_items", [])
    if not isinstance(items, list) or not all(check_confidence(item) for item in items):
        return False
    return True
