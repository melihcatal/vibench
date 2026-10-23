def normalize_line_items(items):
    normalized = []
    for item in items or []:
        normalized.append({
            "description": item.get("description"),
            "quantity": item.get("quantity"),
            "amount": item.get("amount"),
        })
    return normalized


def normalize_expense_record(record):
    record = record or {}
    return {
        "vendor": record.get("vendor") or record.get("merchant"),
        "date": record.get("date"),
        "total": record.get("total"),
        "tax": record.get("tax"),
        "items": normalize_line_items(record.get("items") or record.get("line_items")),
        "notes": record.get("notes"),
        "confidence": record.get("confidence"),
    }


def package_document_result(document_type, fields):
    return {document_type: [fields]}
