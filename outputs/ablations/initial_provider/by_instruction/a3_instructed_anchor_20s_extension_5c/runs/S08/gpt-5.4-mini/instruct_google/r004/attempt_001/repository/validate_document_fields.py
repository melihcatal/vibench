from typing import Any, Dict, List


def validate_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = ["vendor", "date", "total"]
    missing = [field for field in required if not payload.get(field)]
    confidences = payload.get("confidence_scores", {})
    low_confidence = [name for name, score in confidences.items() if float(score) < 0.5]
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
        "provider": "google-cloud-documentai",
    }
