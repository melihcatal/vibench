from document_models import standardize_expense_record


def normalize_expense(extracted: dict) -> dict:
    record = standardize_expense_record(extracted)
    record["normalized"] = True
    return record
