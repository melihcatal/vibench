from __future__ import annotations

from typing import Any, Dict, List


REQUIRED_FIELDS = {
    "invoice": ["vendor", "date", "total"],
    "receipt": ["merchant", "total"],
}


def validate_document_fields(
    document: Dict[str, Any], minimum_confidence: float = 0.5
) -> Dict[str, Any]:
    document_type = document.get("document_type", "")
    fields = document.get("fields", {})
    missing: List[str] = []
    low_confidence: List[str] = []
    for field_name in REQUIRED_FIELDS.get(document_type, []):
        field = fields.get(field_name, {})
        if field.get("value") in (None, ""):
            missing.append(field_name)
            continue
        if float(field.get("confidence", 0.0)) < minimum_confidence:
            low_confidence.append(field_name)
    item_confidences = [
        float(item.get("confidence", 0.0)) for item in document.get("items", [])
    ]
    average_item_confidence = (
        sum(item_confidences) / len(item_confidences) if item_confidences else 0.0
    )
    return {
        "document_type": document_type,
        "is_valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "average_item_confidence": average_item_confidence,
    }
