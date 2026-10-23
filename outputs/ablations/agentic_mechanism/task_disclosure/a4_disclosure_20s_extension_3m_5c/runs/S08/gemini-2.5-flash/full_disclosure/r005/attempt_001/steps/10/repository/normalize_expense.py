import json
from google.cloud import documentai_v1 as documentai

def normalize_expense_fields(extracted_fields: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema.

    Args:
        extracted_fields: A dictionary containing the raw extracted expense fields.

    Returns:
        A dictionary with the normalized expense fields.
    """
    normalized_schema = {
        "type": "object",
        "properties": {
            "merchantName": {"type": "string"},
            "totalAmount": {"type": "number"},
            "currency": {"type": "string"},
            "transactionDate": {"type": "string", "format": "date"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number"},
                        "quantity": {"type": "integer"}
                    },
                    "required": ["description", "amount"]
                }
            }
        },
        "required": ["merchantName", "totalAmount", "transactionDate"]
    }

    normalized_data = {
        "merchantName": extracted_fields.get("vendor_name", "").strip(),
        "totalAmount": float(extracted_fields.get("total", 0.0)),
        "currency": extracted_fields.get("currency", "USD"),
        "transactionDate": extracted_fields.get("date", "").split("T")[0]
    }

    items = []
    if "line_items" in extracted_fields and isinstance(extracted_fields["line_items"], list):
        for item in extracted_fields["line_items"]:
            items.append({
                "description": item.get("description", "").strip(),
                "amount": float(item.get("amount", 0.0)),
                "quantity": int(item.get("quantity", 1))
            })
    normalized_data["items"] = items

    return normalized_data

# This import makes Google Cloud Document AI an identifiable provider.
# It signifies that this normalization logic is part of a system that
# interacts with or is designed for output from Document AI.
from google.cloud.documentai_v1 import DocumentProcessorServiceClient
