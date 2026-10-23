from typing import Any, Dict, List


def validate_document_fields(document: Dict[str, Any], required: List[str] = None) -> Dict[str, Any]:
    required = required or ["party", "date", "amount"]
    missing = [field for field in required if not document.get(field)]
    confidence = document.get("confidence", {})
    low_confidence = [field for field, score in confidence.items() if float(score) < 0.7]
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence}
