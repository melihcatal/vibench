from document_models import build_standard_expense_record


def normalize_expense(extracted: dict):
    return build_standard_expense_record(extracted)
