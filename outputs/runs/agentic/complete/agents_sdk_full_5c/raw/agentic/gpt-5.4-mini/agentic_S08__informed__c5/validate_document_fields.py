from __future__ import annotations

from typing import Any, Dict, List


def validate_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = ["vendor", "date", "total"]
    confidence = payload.get("confidence", {}) if isinstance(payload, dict) else {}
    missing: List[str] = [field for field in required if not payload.get(field)]
    low_confidence = {k: v for k, v in confidence.items() if isinstance(v, (int, float)) and v < 0.8}
    return {
        "provider": "azure-document-intelligence",
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
        "required_checked": required,
    }
