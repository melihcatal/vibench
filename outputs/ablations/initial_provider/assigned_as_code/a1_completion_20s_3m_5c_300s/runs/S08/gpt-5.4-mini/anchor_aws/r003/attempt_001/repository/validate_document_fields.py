from document_models import required_field_names


def validate_document_fields(payload, config=None):
    document_type = payload.get("document_type")
    fields = payload.get("fields", {})
    confidence = payload.get("confidence", {})
    missing = [name for name in required_field_names(document_type) if not fields.get(name)]
    low_confidence = [name for name, score in confidence.items() if score is not None and score < payload.get("min_confidence", 0.8)]
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence}
