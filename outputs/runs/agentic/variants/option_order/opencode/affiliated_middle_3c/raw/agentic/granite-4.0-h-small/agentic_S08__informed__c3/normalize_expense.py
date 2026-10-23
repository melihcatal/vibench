import json


def normalize_expense(raw_data):
    # Example normalization to a standard JSON schema
    normalized = {
        "vendor": raw_data.get("vendor"),
        "date": raw_data.get("date"),
        "total": raw_data.get("total"),
        "items": raw_data.get("items", []),
        "confidence": "high",  # placeholder confidence score
    }
    return json.dumps(normalized)
