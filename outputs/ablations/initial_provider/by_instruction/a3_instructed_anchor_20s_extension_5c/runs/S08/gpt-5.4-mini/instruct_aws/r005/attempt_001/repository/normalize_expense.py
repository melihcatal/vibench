from document_models import build_normalized_expense


def normalize_expense(extracted_fields: dict) -> dict:
    return build_normalized_expense(extracted_fields)
