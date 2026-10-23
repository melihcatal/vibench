from document_models import standardize_expense_record


def normalize_expense(fields: dict) -> dict:
    return standardize_expense_record(fields)
