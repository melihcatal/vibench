from typing import Any, Dict, List


def validate_document_fields(payload: Dict[str, Any], required_fields: List[str] = None, minimum_confidence: float = 0.8) -> Dict[str, Any]:
    required_fields = required_fields or ["vendor", "date", "total"]
    fields = payload.get("fields", {})
    missing = [field for field in required_fields if field not in fields or fields[field] in (None, "")]
    low_confidence = []
    for field, value in fields.items():
        confidence = value.get("confidence") if isinstance(value, dict) else None
        if confidence is not None and confidence < minimum_confidence:
            low_confidence.append(field)
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence}
