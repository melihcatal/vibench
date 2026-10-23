# Provider: AWS Comprehend (Comprehend Medical for health docs, otherwise generic)
# Provider identifier present via import above

import json
from typing import Any, Dict


def validate_document_fields(
    data: Dict[str, Any], required_fields: list[str], min_confidence: float = 0.7
) -> bool:
    """Validate that required fields exist in the extraction result and meet a confidence threshold.
    Returns True if validation passes, otherwise False.
    """
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
        confidence = data.get(f"{field}_confidence")
        if confidence is None or confidence < min_confidence:
            return False
    return True
