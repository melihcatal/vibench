from document_models import normalize_confidence


def validate_document_fields(data):
    required = ["confidence"]
    missing = [field for field in required if field not in data]
    confidence = normalize_confidence(data.get("confidence", 0.0))
    return {"valid": not missing and confidence >= 0.5, "missing": missing, "confidence": confidence}
