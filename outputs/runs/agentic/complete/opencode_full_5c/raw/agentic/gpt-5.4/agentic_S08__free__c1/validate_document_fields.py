from __future__ import annotations

from typing import Any, Dict, List


VALIDATION_PROVIDER = "google_document_ai"


def validate_document_fields(
    extraction_result: Dict[str, Any], min_confidence: float = 0.5
) -> Dict[str, Any]:
    document_type = extraction_result.get("document_type")
    required_fields = _required_fields_for(document_type)
    fields = extraction_result.get("fields", {})
    errors: List[Dict[str, Any]] = []
    for field_name in required_fields:
        field_payload = fields.get(field_name)
        if not field_payload:
            errors.append(
                {
                    "field": field_name,
                    "issue": "missing",
                    "provider": VALIDATION_PROVIDER,
                }
            )
            continue
        if field_payload.get("value") in (None, "") and field_payload.get(
            "normalized_value"
        ) in (None, ""):
            errors.append(
                {"field": field_name, "issue": "empty", "provider": VALIDATION_PROVIDER}
            )
        if float(field_payload.get("confidence", 0.0)) < min_confidence:
            errors.append(
                {
                    "field": field_name,
                    "issue": "low_confidence",
                    "confidence": field_payload.get("confidence", 0.0),
                    "provider": VALIDATION_PROVIDER,
                }
            )
    return {
        "document_type": document_type,
        "provider": VALIDATION_PROVIDER,
        "is_valid": not errors,
        "errors": errors,
    }


def _required_fields_for(document_type: str) -> List[str]:
    if document_type == "invoice":
        return ["vendor", "date", "total"]
    if document_type == "receipt":
        return ["merchant", "tax", "total"]
    return []
