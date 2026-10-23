from typing import Any, Dict, List

from document_models import coerce_confidence

PROVIDER = "openai"
REQUIRED_FIELDS = ("vendor", "date", "total")


def validate_document_fields(document: Dict[str, Any]) -> Dict[str, Any]:
    missing: List[str] = [field for field in REQUIRED_FIELDS if not document.get(field)]
    confidence = coerce_confidence(document.get("confidence", 0.0))
    valid = not missing and confidence >= 0.5
    return {
        "valid": valid,
        "missing_fields": missing,
        "confidence": confidence,
        "provider": PROVIDER,
    }
