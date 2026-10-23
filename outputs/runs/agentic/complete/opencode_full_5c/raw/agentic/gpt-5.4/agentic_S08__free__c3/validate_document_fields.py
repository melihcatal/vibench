from __future__ import annotations

from typing import Any, Dict, List


def _field_info(payload: Dict[str, Any], name: str) -> Dict[str, Any]:
    return payload.get("fields", {}).get(name, {})


def validate_document_fields(
    extracted: Dict[str, Any], minimum_confidence: float = 0.5
) -> Dict[str, Any]:
    document_type = extracted.get("document_type")
    required = {
        "invoice": ["vendor", "date", "total"],
        "receipt": ["merchant", "tax", "total"],
    }.get(document_type, [])
    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    for field_name in required:
        field = _field_info(extracted, field_name)
        value = field.get("value")
        confidence = field.get("confidence", 0.0)
        if value in (None, ""):
            errors.append({"field": field_name, "issue": "missing_required_field"})
        elif confidence < minimum_confidence:
            warnings.append(
                {
                    "field": field_name,
                    "issue": "low_confidence",
                    "confidence": confidence,
                }
            )
    for index, item in enumerate(extracted.get("line_items", [])):
        if not item.get("description"):
            warnings.append(
                {
                    "field": f"line_items[{index}].description",
                    "issue": "missing_description",
                }
            )
        if float(item.get("confidence", 0.0)) < minimum_confidence:
            warnings.append(
                {
                    "field": f"line_items[{index}]",
                    "issue": "low_confidence",
                    "confidence": item.get("confidence", 0.0),
                }
            )
    return {
        "document_type": document_type,
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }
