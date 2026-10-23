def validate_document_fields(document):
    required = ["vendor", "date", "total"]
    missing = [field for field in required if not document.get(field)]
    confidence = document.get("confidence")
    low_confidence = confidence is not None and confidence < 0.8
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
    }
