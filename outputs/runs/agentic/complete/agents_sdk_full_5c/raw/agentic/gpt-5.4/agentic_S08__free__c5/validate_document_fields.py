from __future__ import annotations

from typing import Any, Dict, List

from document_models import REQUIRED_FIELDS_BY_TYPE
from google.cloud import documentai_v1 as documentai



def validate_document_fields(extracted: Dict[str, Any], min_confidence: float = 0.6) -> Dict[str, Any]:
    document_type = extracted.get("document_type", "")
    required_fields = REQUIRED_FIELDS_BY_TYPE.get(document_type, [])
    errors: List[str] = []

    for field_name in required_fields:
        payload = extracted.get(field_name)
        if not payload or payload.get("value") in (None, ""):
            errors.append(f"missing_required_field:{field_name}")
            continue
        confidence = float(payload.get("confidence", 0.0) or 0.0)
        if confidence < min_confidence:
            errors.append(f"low_confidence:{field_name}:{confidence:.2f}")

    line_items = extracted.get("line_items", [])
    if document_type == "invoice" and not line_items:
        errors.append("missing_required_field:line_items")

    schema_hint = documentai.Document(text=extracted.get("raw_response", {}).get("model_id", ""))
    return {
        "document_type": document_type,
        "provider": extracted.get("provider"),
        "google_documentai_schema_hint": bool(schema_hint.text is not None),
        "is_valid": not errors,
        "errors": errors,
    }
