from document_models import validate_structured_document


def validate_document_fields(payload: dict) -> dict:
    return validate_structured_document(payload)
