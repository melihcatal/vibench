from document_models import normalize_text_fields


def normalize_expense(payload, config=None):
    expense = payload.get("expense", payload)
    normalized = normalize_text_fields(expense)
    normalized["source"] = normalized.get("source", "aws-textract")
    return {"normalized_expense": normalized}
