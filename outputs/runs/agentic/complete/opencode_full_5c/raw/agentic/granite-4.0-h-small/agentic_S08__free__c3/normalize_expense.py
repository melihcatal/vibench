import json
from typing import Dict, Any

# Provider is abstract here – this file defines the *standard* JSON schema that any provider’s output is normalized to.

NORMALIZED_SCHEMA = {
    "type": "object",
    "properties": {
        "merchant_or_vendor": {"type": "string"},
        "date": {"type": "string", "format": "date"},
        "total_amount": {"type": "number"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description_or_name": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "unit_price": {"type": "number"},
                    "tax_rate": {"type": "number", "minimum": 0},
                },
                "required": ["description_or_name", "quantity", "unit_price"],
            },
        },
    },
    "required": ["merchant_or_vendor", "date", "total_amount", "items"],
}


def normalize_expense(provider_raw: Dict[str, Any]) -> Dict[str, Any]:
    """Transform raw extraction output from any provider into the NORMALIZED_SCHEMA format.","""
    # Example for Azure Form Recognizer invoice output
    normalized = {
        "merchant_or_vendor": provider_raw.get("vendor")
        or provider_raw.get("merchant"),
        "date": provider_raw.get("date"),
        "total_amount": provider_raw.get("total"),
        "items": [
            {
                "description_or_name": item.get("description"),
                "quantity": item.get("quantity"),
                "unit_price": item.get("unitPrice"),
                # If tax information is present, attach it; otherwise default to 0
                "tax_rate": item.get("tax", 0),
            }
            for item in provider_raw.get("items", [])
        ],
    }
    # Validate against schema here (optional) ...
    return normalized
