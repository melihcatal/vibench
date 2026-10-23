import json

NORMALIZED_SCHEMA = {"vendor": "", "date": "", "total": 0.0, "line_items": []}


def normalize_expense(raw_data):
    """Converts provider-specific raw expense data into NORMALIZED_SCHEMA.
    Args:
        raw_data (dict): Provider raw JSON response.
    Returns:
        dict: Normalized expense following NORMALIZED_SCHEMA.
    """
    # Example for Textract AnalyzeExpense
    normalized = NORMALIZED_SCHEMA.copy()
    normalized["vendor"] = raw_data.get("vendor", "")
    normalized["date"] = raw_data.get("date", "")
    normalized["total"] = float(raw_data.get("total", 0))
    normalized["line_items"] = [
        {
            "description": item.get("description", ""),
            "quantity": item.get("quantity", 0),
            "unit_price": item.get("unit_price", 0.0),
            "total": item.get("total", 0.0),
        }
        for item in raw_data.get("line_items", [])
    ]
    return normalized
