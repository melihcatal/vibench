from document_models import field_content


def normalize_expense(payload, config=None):
    expense = payload.get("expense") or payload
    document_type = expense.get("document_type") or payload.get("document_type") or "expense"
    normalized = {
        "document_type": document_type,
        "vendor": expense.get("vendor") or expense.get("merchant"),
        "date": expense.get("date"),
        "total": expense.get("total"),
        "tax": expense.get("tax"),
        "line_items": expense.get("line_items") or expense.get("items") or [],
        "notes": expense.get("notes"),
    }
    return {"normalized_expense": normalized}
