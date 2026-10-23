import json


def normalize_expense(raw_document):
    # Map provider-specific keys to a common schema
    normalized = {"vendor": "", "date": "", "total": 0.0, "items": []}
    if raw_document.get("vendor") is not None:
        normalized["vendor"] = raw_document["vendor"]
    if raw_document.get("date") is not None:
        normalized["date"] = raw_document["date"]
    # Normalize totals (handle string/float)
    raw_total = raw_document.get("total", 0)
    normalized["total"] = float(raw_total) if raw_total else 0.0
    # Normalize line items
    for item in raw_document.get("line_items", []):
        normalized["items"].append(
            {
                "description": item.get("description", ""),
                "quantity": item.get("quantity", 1),
                "unit_price": float(item.get("unit_price", 0)),
                "amount": float(item.get("amount", 0)),
            }
        )
    return normalized
