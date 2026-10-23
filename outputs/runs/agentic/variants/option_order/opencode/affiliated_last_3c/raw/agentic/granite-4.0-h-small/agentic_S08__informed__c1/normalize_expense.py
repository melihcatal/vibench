import json


def normalize_expense(raw_data: dict) -> dict:
    # Map provider-specific keys to a standardized schema
    normalized = {
        "merchant_or_vendor": raw_data.get("merchant", raw_data.get("vendor", "")),
        "date": raw_data.get("date"),
        "total": raw_data.get("total"),
        "items": [
            {
                "description": line.get("description", ""),
                "quantity": line.get("quantity", 0),
                "unit_price": line.get("unit_price", 0),
                "total": line.get("total", 0),
            }
            for line in raw_data.get("line_items", [])
        ],
    }
    return normalized


if __name__ == "__main__":
    # Example usage with invoice payload
    sample = {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": 123.45,
        "line_items": [
            {
                "description": "Widget A",
                "quantity": 2,
                "unit_price": 10.0,
                "total": 20.0,
            },
            {
                "description": "Widget B",
                "quantity": 1,
                "unit_price": 12.0,
                "total": 12.0,
            },
        ],
    }
    normalized = normalize_expense(sample)
    print(json.dumps(normalized, indent=2))
