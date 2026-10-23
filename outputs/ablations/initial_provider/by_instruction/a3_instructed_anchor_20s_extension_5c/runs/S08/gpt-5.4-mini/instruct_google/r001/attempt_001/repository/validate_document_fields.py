from typing import Any, Dict, List


def validate_document_fields(fields: Dict[str, Any], confidence: Dict[str, float]) -> Dict[str, Any]:
    required = ["merchant", "date", "total"]
    missing = [name for name in required if not fields.get(name)]
    low_confidence = [name for name, score in confidence.items() if score < 0.8]
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence}
