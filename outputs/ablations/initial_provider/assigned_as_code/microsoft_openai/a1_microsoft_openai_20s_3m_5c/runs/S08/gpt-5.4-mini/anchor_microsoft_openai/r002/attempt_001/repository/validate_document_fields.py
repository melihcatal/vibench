def validate_document_fields(payload, config=None):
    document = payload.get("document") or payload
    required_fields = (config or {}).get("required_fields") or ["vendor", "date", "total"]
    min_confidence = (config or {}).get("min_confidence", 0.5)
    fields = document.get("fields") or document
    missing = [name for name in required_fields if not fields.get(name)]
    low_confidence = []
    confidences = document.get("confidences") or {}
    for name in required_fields:
        confidence = confidences.get(name)
        if confidence is not None and confidence < min_confidence:
            low_confidence.append(name)
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence}
