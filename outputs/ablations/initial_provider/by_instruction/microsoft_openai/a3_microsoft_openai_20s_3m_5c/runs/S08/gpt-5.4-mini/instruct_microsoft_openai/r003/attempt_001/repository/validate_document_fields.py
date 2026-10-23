def validate_document_fields(extracted):
    required = ["merchant", "date", "total"]
    missing = [field for field in required if not extracted.get(field)]
    confidence = extracted.get("confidence", 1.0)
    return {"valid": not missing and confidence >= 0.8, "missing": missing, "confidence": confidence}
