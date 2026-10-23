from document_models import validate_required_fields


def validate_document_fields(fields: dict, confidence: float) -> dict:
    result = validate_required_fields(fields, ["vendor", "date", "total"])
    result["confidence_ok"] = confidence >= 0.7
    return result
