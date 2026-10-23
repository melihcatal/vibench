# [SAME-SCENARIO] validate_document_fields.py
# Validates required structured fields and confidence scores

from typing import Any, Dict

REQUIRED_FIELDS = {
    "vendor": lambda v: isinstance(v, str) and v.strip(),
    "date": lambda d: isinstance(d, str) and len(d) == 10 and d[4] == d[7] == "-",
    "total": lambda t: isinstance(t, (int, float)) and t >= 0,
    "line_items": lambda li: (
        isinstance(li, list) and all(isinstance(item, dict) for item in li)
    ),
    "merchant": lambda m: isinstance(m, str) and m.strip(),
    "tax": lambda tx: isinstance(tx, (int, float)) and tx >= 0,
    "items": lambda its: (
        isinstance(its, list) and all(isinstance(item, dict) for item in its)
    ),
}


def validate(fields: Dict[str, Any]) -> bool:
    """Check that all required fields are present and conform to expectations."""
    for field, check in REQUIRED_FIELDS.items():
        value = fields.get(field)
        if value is None or not check(value):
            print(f"Validation failed for field '{field}': {value}")
            return False
    return True


if __name__ == "__main__":
    # Example validation with a full record
    record = {
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
    print("Validation result:", validate(record))
