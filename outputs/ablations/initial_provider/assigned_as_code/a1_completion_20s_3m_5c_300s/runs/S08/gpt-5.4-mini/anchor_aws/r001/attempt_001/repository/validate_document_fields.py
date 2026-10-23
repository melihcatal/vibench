def validate_document_fields(payload, config=None):
    config = config or {}
    required = config.get("required_fields", ["vendor", "date", "total"])
    document = payload.get("document") or payload.get("normalized_expense") or payload
    missing = [field for field in required if not document.get(field)]
    confidence_threshold = config.get("confidence_threshold", 0.8)
    confidence = document.get("confidence", 1.0)
    return {"valid": not missing and confidence >= confidence_threshold, "missing_fields": missing, "confidence": confidence}
