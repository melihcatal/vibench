from typing import Any, Dict, List

from document_models import coerce_confidence


REQUIRED_FIELDS = ["vendor", "date", "total"]


def validate_document_fields(
    extracted: Dict[str, Any], minimum_confidence: float = 0.8
) -> Dict[str, Any]:
    fields = extracted.get("fields", {})
    missing: List[str] = []
    low_confidence: List[str] = []
    for name in REQUIRED_FIELDS:
        item = fields.get(name)
        if not item or item.get("value") in (None, ""):
            missing.append(name)
            continue
        if coerce_confidence(item.get("confidence")) < minimum_confidence:
            low_confidence.append(name)
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
    }
