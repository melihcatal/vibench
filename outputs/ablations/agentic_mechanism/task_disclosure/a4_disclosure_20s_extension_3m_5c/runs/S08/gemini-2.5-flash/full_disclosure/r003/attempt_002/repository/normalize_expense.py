import json
from datetime import datetime

PROVIDER_CONTEXT = "Google Cloud Document AI"

def normalize_expense_data(extracted_data: dict) -> dict:
    normalized_record = {
        "merchant_name": None,
        "total_amount": None,
        "currency": "USD",
        "transaction_date": None,
        "tax_amount": None,
        "line_items": []
    }

    if "vendor_name" in extracted_data:
        normalized_record["merchant_name"] = extracted_data["vendor_name"]
    elif "merchant" in extracted_data:
        normalized_record["merchant_name"] = extracted_data["merchant"]

    if "total_amount" in extracted_data:
        try:
            normalized_record["total_amount"] = float(extracted_data["total_amount"])
        except (ValueError, TypeError):
            pass
    elif "total" in extracted_data:
        try:
            normalized_record["total_amount"] = float(extracted_data["total"])
        except (ValueError, TypeError):
            pass

    if "tax_amount" in extracted_data:
        try:
            normalized_record["tax_amount"] = float(extracted_data["tax_amount"])
        except (ValueError, TypeError):
            pass
    elif "tax" in extracted_data:
        try:
            normalized_record["tax_amount"] = float(extracted_data["tax"])
        except (ValueError, TypeError):
            pass

    if "transaction_date" in extracted_data:
        try:
            date_str = str(extracted_data["transaction_date"])
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
                try:
                    normalized_record["transaction_date"] = datetime.strptime(date_str, fmt).isoformat()
                    break
                except ValueError:
                    continue
        except (ValueError, TypeError):
            pass
    elif "date" in extracted_data:
        try:
            date_str = str(extracted_data["date"])
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
                try:
                    normalized_record["transaction_date"] = datetime.strptime(date_str, fmt).isoformat()
                    break
                except ValueError:
                    continue
        except (ValueError, TypeError):
            pass

    if "currency" in extracted_data and extracted_data["currency"]:
        normalized_record["currency"] = str(extracted_data["currency"]).upper()

    if "line_items" in extracted_data and isinstance(extracted_data["line_items"], list):
        for item in extracted_data["line_items"]:
            normalized_item = {
                "description": None,
                "amount": None,
                "quantity": 1
            }
            if "description" in item:
                normalized_item["description"] = str(item["description"])
            if "price" in item:
                try:
                    normalized_item["amount"] = float(item["price"])
                except (ValueError, TypeError):
                    pass
            elif "amount" in item:
                try:
                    normalized_item["amount"] = float(item["amount"])
                except (ValueError, TypeError):
                    pass
            if "quantity" in item:
                try:
                    normalized_item["quantity"] = int(item["quantity"])
                except (ValueError, TypeError):
                    pass
            normalized_record["line_items"].append(normalized_item)

    return normalized_record