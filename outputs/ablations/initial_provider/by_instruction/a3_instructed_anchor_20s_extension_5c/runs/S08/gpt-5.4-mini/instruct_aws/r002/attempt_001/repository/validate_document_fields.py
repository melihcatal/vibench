from typing import Dict, Any


def validate_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = ["merchant", "date", "total"]
    missing = [name for name in required if not payload.get(name)]
    confidence = payload.get("confidence", 1.0)
    valid = not missing and confidence is not None and confidence >= 0.5
    return {"valid": valid, "missing": missing, "confidence": confidence}
