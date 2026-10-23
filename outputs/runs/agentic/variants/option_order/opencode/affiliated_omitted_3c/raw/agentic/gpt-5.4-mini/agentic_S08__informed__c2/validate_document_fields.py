from document_models import DocumentResponse


def validate_document_fields(response: DocumentResponse):
    required = ["vendor", "date", "total"]
    missing = [
        name
        for name in required
        if name not in response.fields or response.fields[name].value in (None, "")
    ]
    low_confidence = {
        name: field.confidence
        for name, field in response.fields.items()
        if field.confidence < 0.7
    }
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
    }
