from document_models import build_standard_expense_schema


def normalize_expense(payload, config=None):
    config = config or {}
    source = payload.get("invoice") or payload.get("receipt") or payload.get("fields") or payload
    expense = {
        "vendor": source.get("vendor") or source.get("merchant") or "",
        "date": source.get("date", ""),
        "total": source.get("total", ""),
        "tax": source.get("tax", ""),
        "items": source.get("line_items") or source.get("items") or [],
        "notes": source.get("notes", ""),
        "currency": source.get("currency") or config.get("currency", ""),
    }
    return {"expense": build_standard_expense_schema(expense)}
