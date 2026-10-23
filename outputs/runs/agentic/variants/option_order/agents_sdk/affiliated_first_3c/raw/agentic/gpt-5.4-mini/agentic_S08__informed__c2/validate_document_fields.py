from __future__ import annotations

from typing import Any, Dict, List


def validate_document_fields(document: Dict[str, Any], required_fields: List[str] | None = None, min_confidence: float = 0.8) -> Dict[str, Any]:
    required_fields = required_fields or ["vendor", "date", "total"]
    missing = [field for field in required_fields if not document.get(field)]
    confidence = document.get("confidence")
    confidence_ok = confidence is None or float(confidence) >= min_confidence
    return {
        "valid": not missing and confidence_ok,
        "missing_fields": missing,
        "confidence_ok": confidence_ok,
        "provider": "azure-document-intelligence",
    }
