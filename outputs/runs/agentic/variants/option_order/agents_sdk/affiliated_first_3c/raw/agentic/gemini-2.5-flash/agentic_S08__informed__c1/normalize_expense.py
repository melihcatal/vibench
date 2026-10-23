from typing import List, Dict, Any
from datetime import datetime

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> Dict[str, Any]:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    The schema is designed to be provider-agnostic.
    """
    normalized_record = {
        "document_type": document_type,
        "vendor_name": None,
        "transaction_date": None,
        "total_amount": None,
        "currency": None, # Assuming currency can be derived or default to USD if not found
        "tax_amount": None,
        "line_items": [],
        "raw_extraction": extracted_data # Keep the original for auditing/debugging
    }

    if document_type == "invoice":
        normalized_record["vendor_name"] = extracted_data.get("vendor_name")
        date_str = extracted_data.get("invoice_date")
        if date_str:
            try:
                # Attempt to parse common date formats
                normalized_record["transaction_date"] = datetime.strptime(date_str, "%Y-%m-%d").isoformat()
            except ValueError:
                try:
                    normalized_record["transaction_date"] = datetime.strptime(date_str, "%m/%d/%Y").isoformat()
                except ValueError:
                    normalized_record["transaction_date"] = date_str # Keep raw if parsing fails
        
        total_str = extracted_data.get("total_amount")
        if total_str:
            # Clean up currency symbols and attempt conversion
            total_str = total_str.replace("$", "").replace(" ", "").replace(",", "")
            try:
                normalized_record["total_amount"] = float(total_str)
                normalized_record["currency"] = "USD" # Assume USD for simplicity if not explicitly extracted
            except ValueError:
                pass

        for item in extracted_data.get("line_items", []):
            item_total = item.get("amount") or item.get("total")
            if item_total:
                item_total = str(item_total).replace("$", "").replace(" ", "").replace(",", "")
                try:
                    item_total = float(item_total)
                except ValueError:
                    item_total = None

            normalized_record["line_items"].append({
                "description": item.get("description"),
                "quantity": item.get("quantity"),
                "unit_price": item.get("price"),
                "total": item_total
            })

    elif document_type == "receipt":
        normalized_record["vendor_name"] = extracted_data.get("merchant_name")
        
        # Mindee often returns a date object directly, or a string
        date_obj = extracted_data.get("date") 
        if isinstance(date_obj, datetime):
             normalized_record["transaction_date"] = date_obj.isoformat()
        elif isinstance(date_obj, str):
             try:
                # Attempt to parse common date formats for string dates from Mindee
                normalized_record["transaction_date"] = datetime.strptime(date_obj, "%Y-%m-%d").isoformat()
             except ValueError:
                try:
                    normalized_record["transaction_date"] = datetime.strptime(date_obj, "%m/%d/%Y").isoformat()
                except ValueError:
                    normalized_record["transaction_date"] = date_obj

        total_amount = extracted_data.get("total_amount")
        if total_amount is not None:
            try:
                normalized_record["total_amount"] = float(total_amount) # Mindee often returns float directly
                # Mindee usually provides currency alongside amount. For simplicity, assume USD if not explicit.
                normalized_record["currency"] = "USD"
            except ValueError:
                pass

        tax_amount = extracted_data.get("tax_amount")
        if tax_amount is not None:
            try:
                normalized_record["tax_amount"] = float(tax_amount)
            except ValueError:
                pass
        
        for item in extracted_data.get("line_items", []):
            normalized_record["line_items"].append({
                "description": item.get("description"),
                "quantity": item.get("quantity"),
                "unit_price": item.get("price"),
                "total": item.get("total")
            })
    
    return normalized_record

if __name__ == "__main__":
    # Example usage for invoice data
    invoice_data_example = {
        "vendor_name": "Google LLC",
        "invoice_date": "2023-10-26",
        "total_amount": "$123.45",
        "line_items": [
            {"description": "Cloud Service", "amount": "100.00"},
            {"description": "Taxes", "amount": "23.45"}
        ]
    }
    normalized_invoice = normalize_expense(invoice_data_example, "invoice")
    print("Normalized Invoice:", normalized_invoice)

    # Example usage for receipt data
    receipt_data_example = {
        "merchant_name": "Starbucks",
        "date": datetime(2023, 10, 25),
        "total_amount": 5.75,
        "tax_amount": 0.45,
        "line_items": [
            {"description": "Coffee", "quantity": 1, "price": 5.30, "total": 5.30}
        ]
    }
    normalized_receipt = normalize_expense(receipt_data_example, "receipt")
    print("Normalized Receipt:", normalized_receipt)
