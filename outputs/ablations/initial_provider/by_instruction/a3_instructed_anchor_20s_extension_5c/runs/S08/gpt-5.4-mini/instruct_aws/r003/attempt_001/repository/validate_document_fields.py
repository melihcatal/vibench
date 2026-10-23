from typing import Any, Dict, List


def validate_document_fields(fields: Dict[str, Any], required: List[str] = None, min_confidence: float = 0.5) -> Dict[str, Any]:
    required = required or ["vendor", "date", "total"]
    confidence = fields.get("confidence", {})
    missing = [name for name in required if not fields.get(name)]
    low_confidence = [name for name in required if confidence.get(name, 1.0) < min_confidence]
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
    }
