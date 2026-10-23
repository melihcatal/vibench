import json
from typing import Dict, Any

# Provider is abstract – this module validates *any* provider's extracted fields.

REQUIRED_FIELDS = {"vendor", "merchant", "date", "total", "items"}

CONFIDENCE_THRESHOLD = 0.80


def validate_document_fields(extracted: Dict[str, Any]) -> bool:
    """Check that all required structured fields exist and have sufficient confidence.","""

    # Example: extract confidence from the payload (most providers embed it)
    # For demo we assume each top‑level field has a "confidence" key (could be nested)
    def get_confidence(val):
        # Simple heuristic: if a number field is present as "confidence", use it;
        # otherwise assume a default good confidence.
        return val.get("confidence", 1.0)

    if not set(extracted.keys()) >= REQUIRED_FIELDS:
        return False

    # Verify confidence for each required field
    for field in REQUIRED_FIELDS:
        confidence = get_confidence(extracted.get(field, {}))
        if confidence < CONFIDENCE_THRESHOLD:
            return False
    return True
