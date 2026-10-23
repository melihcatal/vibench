from document_models import StructuredField, StructuredDocumentResponse


def validate_document_fields(response: StructuredDocumentResponse):
    required = {"vendor", "date", "total"}
    present = {f.name.lower() for f in response.fields}
    missing = sorted(required - present)
    low_confidence = [f.name for f in response.fields if f.confidence < 0.7]
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
    }
