from document_models import ensure_required_fields


def validate_document_fields(payload: dict) -> dict:
    missing = ensure_required_fields(payload, ["merchant", "date", "total"])
    return {"valid": not missing, "missing_fields": missing, "min_confidence": 0.8}
