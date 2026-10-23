def normalize_expense(raw):
    """Convert raw extraction dicts (invoice or receipt) to a common schema:
    {
        "vendor_or_merchant": str,
        "date": str,
        "total": str,
        "items": [dict with keys: description, price/quantity/unit_price],
        "schema_version": "1.0"
    }
    """
    normalized = {
        "vendor_or_merchant": raw.get("vendor") or raw.get("merchant"),
        "date": raw.get("invoice_date") or raw.get("date"),
        "total": raw.get("total"),
        "items": raw.get("line_items") or raw.get("items", []),
        "schema_version": "1.0"
    }
    return normalized
