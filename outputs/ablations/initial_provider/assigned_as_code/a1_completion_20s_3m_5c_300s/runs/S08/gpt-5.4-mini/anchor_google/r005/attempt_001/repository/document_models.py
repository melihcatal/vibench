def normalize_line_item(item):
    return {"description": item.get("description"), "quantity": item.get("quantity"), "amount": item.get("amount")}


def normalize_expense_record(record):
    return {
        "vendor": record.get("vendor"),
        "date": record.get("date"),
        "total": record.get("total"),
        "currency": record.get("currency"),
        "line_items": [normalize_line_item(item) for item in record.get("line_items", [])],
    }
