from typing import Any, Dict

# Define a standard JSON schema for normalized expense records
NORMALIZED_EXPENSE_SCHEMA = {
    "type": "object",
    "properties": {
        "expense_id": {"type": "string"},
        "vendor": {"type": "string"},
        "merchant": {"type": "string"},
        "date": {"type": "string", "format": "date"},
        "total_amount": {"type": "number"},
        "currency": {"type": "string"},
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "quantity": {"type": "number"},
                    "unit_price": {"type": "number"},
                    "amount": {"type": "number"}
                },
                "required": ["description", "quantity", "unit_price", "amount"]
            }
        },
        "tax_amount": {"type": "number"},
        "confidence": {"type": "number"}
    },
    "required": ["expense_id", "vendor", "total_amount", "line_items"]
}


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    """Convert provider-specific extraction result to the standard schema."""
    # Example mapping - adapt to actual provider response structure
    expense = {
        "expense_id": extracted.get("id", "").replace("-", "_"),
        "vendor": extracted.get("vendor", "").strip(),
        "merchant": extracted.get("merchant", extracted.get("vendor", "")).strip(),
        "date": extracted.get("date", ""),
        "total_amount": extracted.get("total", 0.0),
        "currency": extracted.get("currency", "USD"),
        "line_items": [
            {
                "description": item.get("description", ""),
                "quantity": item.get("quantity", 1),
                "unit_price": item.get("price", 0.0),
                "amount": item.get("amount", 0.0)
            }
            for item in extracted.get("line_items", [])
        ],
        "tax_amount": extracted.get("tax", 0.0),
        "confidence": extracted.get("confidence", 0.0)
    }
    return expense