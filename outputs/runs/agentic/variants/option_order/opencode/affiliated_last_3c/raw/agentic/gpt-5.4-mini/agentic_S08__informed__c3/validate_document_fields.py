def validate_document_fields(payload: dict) -> dict:
    required = ["vendor", "date", "total"]
    missing = [key for key in required if not payload.get(key)]
    confidence = payload.get("confidence")
    ok = not missing and (confidence is None or confidence >= 0.5)
    return {"valid": ok, "missing": missing, "confidence": confidence}
