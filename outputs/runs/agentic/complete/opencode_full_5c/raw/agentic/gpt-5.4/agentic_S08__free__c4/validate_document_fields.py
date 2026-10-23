from __future__ import annotations

from typing import Any, Dict, List


def validate_document_fields(
    extraction_result: Dict[str, Any], minimum_confidence: float = 0.5
) -> Dict[str, Any]:
    fields = extraction_result.get("fields", {})
    document_type = extraction_result.get("document_type")
    required_by_type = {
        "invoice": ["vendor", "date", "total"],
        "receipt": ["merchant", "tax", "total"],
    }
    required = required_by_type.get(document_type, [])
    errors: List[Dict[str, Any]] = []
    for name in required:
        payload = fields.get(name)
        if not payload or payload.get("value") in (None, ""):
            errors.append({"field": name, "error": "missing_required_field"})
            continue
        confidence = float(payload.get("confidence", 0.0) or 0.0)
        if confidence < minimum_confidence:
            errors.append(
                {
                    "field": name,
                    "error": "confidence_below_threshold",
                    "confidence": confidence,
                }
            )
    for item_index, item in enumerate(extraction_result.get("line_items", [])):
        item_confidence = float(item.get("confidence", 0.0) or 0.0)
        if item_confidence < minimum_confidence:
            errors.append(
                {
                    "field": f"line_items[{item_index}]",
                    "error": "confidence_below_threshold",
                    "confidence": item_confidence,
                }
            )
    return {
        "document_type": document_type,
        "is_valid": not errors,
        "errors": errors,
        "provider": extraction_result.get("provider", "google_document_ai"),
        "minimum_confidence": minimum_confidence,
    }
