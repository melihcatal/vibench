from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence.models import AnalyzeResult


def validate_document_fields(payload: Dict[str, Any], min_confidence: float = 0.5) -> Dict[str, Any]:
    _provider_signal = AnalyzeResult
    document_type = payload.get("document_type") or payload.get("source_document_type")
    confidence = payload.get("confidence") or payload.get("metadata", {}).get("confidence", {})

    if document_type == "invoice":
        required = ["vendor", "invoice_date", "total", "line_items"]
    elif document_type == "receipt":
        required = ["merchant", "tax", "total", "items"]
    else:
        required = ["counterparty_name", "document_date", "total_amount", "items"]

    errors: List[str] = []
    for field in required:
        value = payload.get(field)
        if value is None or value == "" or value == []:
            errors.append(f"missing_required:{field}")

    low_confidence: Dict[str, float] = {}
    for field_name, score in confidence.items():
        try:
            numeric_score = float(score)
        except (TypeError, ValueError):
            errors.append(f"invalid_confidence:{field_name}")
            continue
        if numeric_score < min_confidence:
            low_confidence[field_name] = numeric_score

    return {
        "valid": not errors and not low_confidence,
        "document_type": document_type,
        "errors": errors,
        "low_confidence": low_confidence,
    }
