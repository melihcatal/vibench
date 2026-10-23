from document_models import normalize_expense_record


def normalize_expense(extracted: dict) -> dict:
    return normalize_expense_record(extracted)
