# [SAME-SCENARIO] normalize_expense.py
# Normalizes extracted expense fields into a standard JSON schema

from typing import Any, Dict

NORMALIZED_SCHEMA = {
    "vendor": str,
    "date": str,
    "total": float,
    "line_items": list,
    "merchant": str,
    "tax": float,
    "items": list,
}


def normalize(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Convert provider-specific fields into the canonical expense schema."""
    normalized = {
        "vendor": fields.get("vendor", ""),
        "date": fields.get("date", ""),
        "total": fields.get("total", 0.0),
        "line_items": fields.get("line_items", []),
        "merchant": fields.get("merchant", ""),
        "tax": fields.get("tax", 0.0),
        "items": fields.get("items", []),
    }
    # Basic validation
    assert isinstance(normalized["vendor"], str)
    assert isinstance(normalized["date"], str)
    assert isinstance(normalized["total"], (int, float))
    assert isinstance(normalized["line_items"], list)
    assert isinstance(normalized["merchant"], str)
    assert isinstance(normalized["tax"], (int, float))
    assert isinstance(normalized["items"], list)
    return normalized


if __name__ == "__main__":
    # Demo with dummy data
    raw = {
        "vendor": "Acme Corp",
        "date": "2024-09-01",
        "total": 123.45,
        "line_items": [
            {"description": "Widget", "quantity": 2, "unit_price": 45.0, "total": 90.0},
            {
                "description": "Gadget",
                "quantity": 1,
                "unit_price": 33.45,
                "total": 33.45,
            },
        ],
        "merchant": "Corner Store",
        "tax": 8.9,
        "items": [
            {"description": "Widget", "quantity": 2, "total": 90.0},
            {"description": "Gadget", "quantity": 1, "total": 33.45},
        ],
    }
    print(normalize(raw))
