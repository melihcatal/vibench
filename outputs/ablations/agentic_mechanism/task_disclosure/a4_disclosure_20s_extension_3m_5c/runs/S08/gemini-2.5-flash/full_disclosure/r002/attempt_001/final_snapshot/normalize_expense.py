from google.cloud import storage
import json

def normalize_expense_fields(extracted_data: dict) -> dict:
    storage_client = storage.Client()
    
    # In a real application, the schema would be fetched from Google Cloud Storage
    # using the storage_client and a specific bucket/blob.
    # For this exercise, a default schema is defined directly.
    standard_schema = {
        "type": "object",
        "properties": {
            "merchant_name": {"type": "string"},
            "transaction_date": {"type": "string", "format": "date"},
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
                        "item_total": {"type": "number"}
                    },
                    "required": ["description", "item_total"]
                }
            }
        },
        "required": ["merchant_name", "transaction_date", "total_amount", "currency"]
    }
    
    normalized_data = {}

    if "vendor" in extracted_data:
        normalized_data["merchant_name"] = extracted_data["vendor"]
    elif "merchant" in extracted_data:
        normalized_data["merchant_name"] = extracted_data["merchant"]
    
    if "date" in extracted_data:
        normalized_data["transaction_date"] = extracted_data["date"]
        
    if "total" in extracted_data:
        normalized_data["total_amount"] = float(extracted_data["total"])
        
    normalized_data["currency"] = extracted_data.get("currency", "USD")

    if "line_items" in extracted_data and isinstance(extracted_data["line_items"], list):
        normalized_data["line_items"] = []
        for item in extracted_data["line_items"]:
            normalized_item = {
                "description": item.get("description"),
                "quantity": item.get("quantity"),
                "unit_price": item.get("unit_price"),
                "item_total": item.get("item_total")
            }
            normalized_data["line_items"].append({k: v for k, v in normalized_item.items() if v is not None})
    
    return normalized_data
