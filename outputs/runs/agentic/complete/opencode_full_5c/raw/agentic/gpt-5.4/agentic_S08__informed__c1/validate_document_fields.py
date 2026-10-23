from __future__ import annotations

from document_models import average_confidence


def validate_document_fields(
    payload: dict, document_type: str, min_confidence: float = 0.6
) -> dict:
    if document_type == "invoice":
        required = ["vendor", "invoice_date", "total"]
        items = payload.get("line_items", [])
    else:
        required = ["merchant", "tax", "total"]
        items = payload.get("items", [])

    missing_fields = []
    field_confidences = []
    low_confidence_fields = []

    for field_name in required:
        field_payload = payload.get(field_name) or {}
        value = field_payload.get("value")
        confidence = field_payload.get("confidence")
        if value in (None, "", []):
            missing_fields.append(field_name)
        if confidence is not None:
            field_confidences.append(confidence)
            if confidence < min_confidence:
                low_confidence_fields.append(field_name)

    for index, item in enumerate(items):
        confidence = item.get("confidence")
        if confidence is not None:
            field_confidences.append(confidence)
            if confidence < min_confidence:
                low_confidence_fields.append(f"item_{index}")

    overall_confidence = average_confidence(field_confidences)
    return {
        "is_valid": not missing_fields and not low_confidence_fields,
        "missing_fields": missing_fields,
        "low_confidence_fields": low_confidence_fields,
        "overall_confidence": overall_confidence,
    }
