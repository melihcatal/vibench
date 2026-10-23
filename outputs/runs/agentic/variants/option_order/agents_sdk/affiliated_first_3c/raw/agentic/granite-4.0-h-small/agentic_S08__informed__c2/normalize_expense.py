import json

def normalize_expense(raw_fields):
    """
    Convert raw extraction results to a standard schema:
    {
        "vendor": str,
        "amount": float,
        "currency": str,
        "date": str,
        "line_items": List[Dict[description, price, quantity]],
        "metadata": Dict
    }
    """
    normalized = {
        "vendor": raw_fields.get("vendor", "UNKNOWN_VENDOR"),
        "amount": raw_fields.get("total", 0.0),  # fallback default
        "currency": raw_fields.get("currency", "USD"),
        "date": raw_fields.get("date", "1900-01-01"),
        "line_items": raw_fields.get("line-items", []),
        "metadata": {}
    }
    return normalized
