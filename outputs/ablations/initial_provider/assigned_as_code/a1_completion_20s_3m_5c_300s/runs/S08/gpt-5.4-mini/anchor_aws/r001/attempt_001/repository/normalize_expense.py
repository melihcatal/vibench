from document_models import build_expense_schema, normalize_field_text


def normalize_expense(payload, config=None):
    config = config or {}
    source = payload.get("expense") or payload.get("invoice") or payload.get("receipt") or {}
    record = {
        "vendor": source.get("vendor") or source.get("merchant"),
        "date": source.get("date"),
        "total": source.get("total"),
        "currency": source.get("currency") or config.get("currency", "USD"),
        "notes": source.get("notes") or source.get("memo"),
        "items": source.get("line_items") or source.get("items") or [],
    }
    return {"normalized_expense": build_expense_schema(record)}
