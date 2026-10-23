from __future__ import annotations

from typing import Any, Dict, List

from document_models import average_confidence, safe_float


REQUIRED_BY_TYPE = {
    "invoice": ["vendor", "invoice_date", "total", "line_items"],
    "receipt": ["merchant", "tax", "total", "line_items"],
}


def validate_document_fields(extracted: Dict[str, Any], minimum_confidence: float = 0.6) -> Dict[str, Any]:
    doc_type = extracted.get("document_type", "invoice")
    required = REQUIRED_BY_TYPE.get(doc_type, [])
    missing: List[str] = []
    for field in required:
        value = extracted.get(field)
        if value is None or value == "" or value == []:
            missing.append(field)

    confidence_map = extracted.get("source_confidence", {}) or {}
    low_confidence = [
        name for name, score in confidence_map.items() if safe_float(score) is not None and float(score) < minimum_confidence
    ]
    return {
        "document_type": doc_type,
        "is_valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "average_confidence": average_confidence({k: float(v) for k, v in confidence_map.items() if v is not None}),
        "provider": extracted.get("provider"),
    }
