# [SAME-SCENARIO] normalize_expense.py
# Normalizes extracted fields into a standard JSON schema


def normalize_expense(raw_data: dict) -> dict:
    """
    Normalizes data from various sources (invoice, receipt) to a common schema:
    {
        "vendor": str,
        "merchant": str,
        "date": str,
        "total": float,
        "tax": float,
        "items": [str],
        "confidence": float
    }
    """
    normalized = {
        "vendor": raw_data.get("vendor") or raw_data.get("merchant"),
        "date": raw_data.get("date"),
        "total": float(raw_data.get("total", 0)),
        "tax": float(raw_data.get("tax", 0)),
        "items": raw_data.get("line_items", []) or raw_data.get("items", []),
        "confidence": raw_data.get("confidence", 1.0),
    }
    # Sanitize numeric fields
    for key in ["total", "tax"]:
        try:
            normalized[key] = float(normalized[key])
        except (TypeError, ValueError):
            normalized[key] = 0.0
    return normalized
