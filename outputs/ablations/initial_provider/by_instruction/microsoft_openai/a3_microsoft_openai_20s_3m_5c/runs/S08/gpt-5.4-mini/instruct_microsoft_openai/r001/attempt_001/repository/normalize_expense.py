from document_client import standardize_expense_payload


def normalize_expense(extracted_fields):
    return standardize_expense_payload(extracted_fields)
