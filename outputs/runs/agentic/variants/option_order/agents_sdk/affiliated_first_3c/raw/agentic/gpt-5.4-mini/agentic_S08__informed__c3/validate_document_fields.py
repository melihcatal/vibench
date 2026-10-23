from __future__ import annotations

from typing import Any, Dict, List

from document_models import coerce_float, ensure_text


def validate_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = ["vendor", "date", "total"]
    missing: List[str] = []
    for field in required:
        if not ensure_text(payload.get(field)):
            missing.append(field)
    confidence = coerce_float(payload.get("confidence"), 0.0)
    field_confidences = payload.get("field_confidences", {}) or {}
    low_confidence = [name for name, value in field_confidences.items() if coerce_float(value, 0.0) < 0.8]
    return {
        "valid": not missing and confidence >= 0.5,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "confidence": confidence,
        "provider": payload.get("provider", "azure-document-intelligence"),
    }
