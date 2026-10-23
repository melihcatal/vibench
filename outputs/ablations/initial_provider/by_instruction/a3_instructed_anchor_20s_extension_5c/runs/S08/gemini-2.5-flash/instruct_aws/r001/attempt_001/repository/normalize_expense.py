import json
from typing import Dict, Any

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> Dict[str, Any]:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    """
    normalized_record = {
        "document_type": document_type,
        "vendor_name": None,
        "transaction_date": None,
        "total_amount": None,
        "currency": None,  # Assuming currency is not extracted in previous steps, add as placeholder
        "line_items": [],
        "tax_amount": None,
        "raw_extraction": extracted_data
    }

    if document_type == "invoice":
        normalized_record["vendor_name"] = extracted_data.get("vendor")
        normalized_record["transaction_date"] = extracted_data.get("date")
        normalized_record["total_amount"] = extracted_data.get("total")
        for item in extracted_data.get("line_items", []):
            normalized_record["line_items"].append({
                "description": item.get("item"),
                "quantity": item.get("quantity"),
                "unit_price": item.get("price"),
                "total": item.get("amount")
            })

    elif document_type == "receipt":
        normalized_record["vendor_name"] = extracted_data.get("merchant")
        # Assuming receipt extraction also provides a date, if not, it would be added here
        normalized_record["transaction_date"] = extracted_data.get("date") # Placeholder, assuming date will be extracted
        normalized_record["total_amount"] = extracted_data.get("total")
        normalized_record["tax_amount"] = extracted_data.get("tax")
        for item in extracted_data.get("items", []):
            normalized_record["line_items"].append({
                "description": item.get("description"),
                "quantity": item.get("quantity"),
                "unit_price": item.get("price"),
                "total": None # Placeholder, Textract `analyze_expense` provides price, but not always total per item directly
            })

    return normalized_record
