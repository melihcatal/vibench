from __future__ import annotations

from typing import Any, Dict, List

from document_client import confidence_value

PROVIDER_NAME = "azure-ai-documentintelligence"
REQUIRED_FIELDS = ("vendor", "date", "total")


def validate_document_fields(payload: Dict[str, Any], min_confidence: float = 0.75) -> Dict[str, Any]:
    missing: List[str] = [field for field in REQUIRED_FIELDS if not payload.get(field)]
    confidences = {key: confidence_value(value) for key, value in payload.items() if key.endswith("_confidence") or key == "confidence"}
    low_confidence = {key: value for key, value in confidences.items() if value is not None and value < min_confidence}
    return {
        "provider": PROVIDER_NAME,
        "is_valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
    }
