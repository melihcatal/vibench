from document_models import normalize_fields


def validate_document_fields(payload: dict):
    required = ["merchant", "date", "total"]
    missing = [field for field in required if not payload.get(field)]
    confidence = payload.get("confidence")
    ok = not missing and (confidence is None or confidence >= 0.5)
    return normalize_fields({"valid": ok, "missing": missing, "confidence": confidence})
