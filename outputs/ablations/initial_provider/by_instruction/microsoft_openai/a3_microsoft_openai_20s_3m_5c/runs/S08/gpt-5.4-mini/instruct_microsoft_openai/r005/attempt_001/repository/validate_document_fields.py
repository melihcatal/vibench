from document_models import normalize_confidence


REQUIRED_FIELDS = ("vendor", "date", "total")


def validate_document_fields(data):
    missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
    confidence = normalize_confidence(data.get("confidence", 0.0))
    return {"valid": not missing and confidence >= 0.5, "missing_fields": missing, "confidence": confidence}
