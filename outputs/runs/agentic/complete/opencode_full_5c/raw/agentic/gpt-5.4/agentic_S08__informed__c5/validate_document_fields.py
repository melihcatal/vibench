from __future__ import annotations

from typing import Any, Dict, List

from document_models import ValidationResult


def validate_document_fields(
    extracted_document: Dict[str, Any], minimum_confidence: float = 0.5
) -> Dict[str, Any]:
    document_type = extracted_document.get("document_type")
    fields = extracted_document.get("fields", {})
    required_by_type = {
        "invoice": ["vendor", "date", "total"],
        "receipt": ["merchant", "tax", "total"],
    }
    issues: List[Dict[str, Any]] = []
    for field_name in required_by_type.get(document_type, []):
        field_payload = fields.get(field_name) or {}
        value = field_payload.get("value")
        confidence = float(field_payload.get("confidence", 0.0) or 0.0)
        if value in (None, "", []):
            issues.append({"field": field_name, "message": "missing required value"})
        if confidence < minimum_confidence:
            issues.append(
                {
                    "field": field_name,
                    "message": f"confidence below threshold {minimum_confidence}",
                }
            )
    for index, item in enumerate(extracted_document.get("line_items", [])):
        if not item.get("description"):
            issues.append(
                {
                    "field": f"line_items[{index}].description",
                    "message": "missing line item description",
                }
            )
    return ValidationResult(valid=not issues, issues=issues).to_dict()
