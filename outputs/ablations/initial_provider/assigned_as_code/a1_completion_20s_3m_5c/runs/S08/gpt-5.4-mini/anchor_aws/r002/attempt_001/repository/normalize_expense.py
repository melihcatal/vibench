from document_models import normalize_expense_schema


def normalize_expense(payload, config=None):
    config = config or {}
    expense = payload.get("expense", payload)
    normalized = normalize_expense_schema(expense)
    normalized["currency"] = config.get("currency", expense.get("currency", "USD"))
    return {"normalized_expense": normalized}
