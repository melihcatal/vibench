from typing import Any, Dict, List


def validate_document_fields(document: Dict[str, Any]) -> Dict[str, Any]:
    required = ["vendor", "date", "total"]
    missing = [name for name in required if not document.get(name)]
    confidences = document.get("confidences", {})
    low_confidence = [name for name, score in confidences.items() if score < 0.8]
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
    }
