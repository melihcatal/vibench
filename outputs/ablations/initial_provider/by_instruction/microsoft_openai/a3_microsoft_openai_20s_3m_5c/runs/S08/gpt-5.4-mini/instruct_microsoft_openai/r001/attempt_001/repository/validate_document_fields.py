from document_models import normalize_confidence


def validate_document_fields(fields, confidences, required_fields=None, minimum_confidence=0.7):
    required_fields = required_fields or ["vendor", "date", "total"]
    missing = [name for name in required_fields if not fields.get(name)]
    low_confidence = [name for name in required_fields if normalize_confidence(confidences.get(name)) < minimum_confidence]
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence}
