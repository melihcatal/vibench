import json
from typing import Dict, Any

# Simple JSON-schema matcher for normalized expense records.
NORMALIZED_SCHEMA = {
    "type": "object",
    "properties": {
        "vendor": {"type": "string"},
        "merchant": {"type": "string"},
        "date": {"type": "string", "format": "date"},
        "total": {"type": "number"},
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "amount": {"type": "number"},
                },
                "required": ["description", "amount"],
            },
        },
    },
    "required": ["vendor", "total", "line_items"],
}


def normalize_expense(expense_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert raw extraction payloads (from same-scenario files) into a standard normalized schema.
    Preference:
        - For invoices, keep 'vendor' + 'line_items'.
        - For receipts, keep 'merchant' + 'line_items'.
    Any missing fields default to None.
    """
    if "vendor" in expense_data:
        # Invoice payload
        norm = {
            "vendor": expense_data.get("vendor"),
            "date": expense_data.get("date"),
            "total": float(expense_data.get("total", 0)),
            "line_items": [
                {
                    "description": item.get("description", ""),
                    "amount": float(item.get("amount", 0)),
                }
                for item in expense_data.get("line_items", [])
            ],
        }
    elif "merchant" in expense_data:
        # Receipt payload
        norm = {
            "merchant": expense_data.get("merchant"),
            "date": expense_data.get("date"),
            "total": float(expense_data.get("total", 0)),
            "line_items": [
                {
                    "description": item.get("description", ""),
                    "amount": float(item.get("amount", 0)),
                }
                for item in expense_data.get("line_items", [])
            ],
        }
    else:
        raise ValueError("Unexpected expense structure")
    return norm
