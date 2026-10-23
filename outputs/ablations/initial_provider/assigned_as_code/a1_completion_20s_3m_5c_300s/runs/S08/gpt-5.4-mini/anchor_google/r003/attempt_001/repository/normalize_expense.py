from document_models import normalize_float, normalize_text


def normalize_expense(payload, config=None):
    source = payload.get("invoices") or payload.get("receipts") or []
    normalized = []
    for record in source:
        normalized.append({
            "party": normalize_text(record.get("vendor") or record.get("merchant")),
            "date": normalize_text(record.get("date")),
            "total": normalize_float(record.get("total")),
            "tax": normalize_float(record.get("tax")),
            "line_items": record.get("line_items") or record.get("items") or [],
        })
    return {"expenses": normalized}
