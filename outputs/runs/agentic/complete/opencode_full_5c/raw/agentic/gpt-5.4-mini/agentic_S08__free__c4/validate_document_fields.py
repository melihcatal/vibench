def validate_document_fields(document, minimum_confidence=0.8):
    required = ["vendor", "date", "total"]
    missing = [field for field in required if not document.get(field)]
    confidence = document.get("confidence_scores", {})
    low_confidence = [
        field for field, score in confidence.items() if score < minimum_confidence
    ]
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
    }
