from typing import Any, Dict
import json


def normalize_expense(raw_data: dict) -> dict:
    """Normalize extracted expense fields into a common JSON schema.

    Expected keys:
      - vendor / merchant
      - date
      - total
      - items / line_items
    """
    normalized = {
        "vendor": raw_data.get("vendor") or raw_data.get("merchant"),
        "date": raw_data.get("date"),
        "total": float(raw_data.get("total", 0)),
        "items": [],
    }
    # Support both invoice line_items and receipt items
    items = raw_data.get("line_items") or raw_data.get("items")
    if items:
        for item in items:
            normalized["items"].append(
                {
                    "description": item.get("description") or item.get("name"),
                    "quantity": item.get("quantity", 1),
                    "unit_price": float(item.get("unit_price", 0)),
                    "total": float(item.get("total", 0)),
                }
            )
    return normalized


# Example usage (for unit testing)
if __name__ == "__main__":
    sample = {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": "125.50",
        "line_items": [
            {
                "description": "Widget A",
                "quantity": 2,
                "unit_price": "45.00",
                "total": "90.00",
            },
            {
                "description": "Widget B",
                "quantity": 1,
                "unit_price": "35.50",
                "total": "35.50",
            },
        ],
    }
    print(json.dumps(normalize_expense(sample), indent=2))
