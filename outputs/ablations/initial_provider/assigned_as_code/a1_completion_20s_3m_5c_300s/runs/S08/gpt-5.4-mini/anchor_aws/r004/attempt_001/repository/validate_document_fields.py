from document_models import field_confidence_map


def validate_document_fields(payload, config=None):
    document = payload.get("document", payload)
    required = (config or {}).get("required_fields", ["vendor", "date", "total"])
    confidence_threshold = float((config or {}).get("confidence_threshold", 0.8))
    fields = document.get("fields", document)
    confidences = field_confidence_map(document.get("confidences", {}))
    missing = [name for name in required if not fields.get(name)]
    low_confidence = [name for name in required if confidences.get(name, 1.0) < confidence_threshold]
    return {"valid": not missing and not low_confidence, "missing_fields": missing, "low_confidence_fields": low_confidence}
