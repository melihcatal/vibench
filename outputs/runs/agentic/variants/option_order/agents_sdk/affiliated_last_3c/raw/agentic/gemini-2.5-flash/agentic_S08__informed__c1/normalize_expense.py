import json

def normalize_expense(extracted_data: dict, document_type: str) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    
    Args:
        extracted_data: A dictionary containing fields extracted by an OCR service.
        document_type: The type of document (e.g., 'invoice', 'receipt').
        
    Returns:
        A dictionary representing the normalized expense record.
    """
    normalized_record = {
        "document_type": document_type,
        "vendor_name": None,
        "transaction_date": None,
        "total_amount": None,
        "currency": None, # Assuming currency can be derived or added later
        "line_items": [],
        "tax_amount": None,
        "notes": None, # For later steps like summarization or translation
        "confidence_scores": {} # To store confidence scores if available
    }

    if document_type == "invoice":
        normalized_record["vendor_name"] = extracted_data.get("vendor_name")
        normalized_record["transaction_date"] = extracted_data.get("invoice_date")
        normalized_record["total_amount"] = extracted_data.get("total_amount")
        # Add logic to parse line items from extracted_data.get("line_items")

    elif document_type == "receipt":
        normalized_record["vendor_name"] = extracted_data.get("merchant_name")
        # Assuming receipt date field is similar or needs separate handling
        normalized_record["transaction_date"] = extracted_data.get("receipt_date") # Placeholder, adjust as per actual extraction
        normalized_record["tax_amount"] = extracted_data.get("tax_amount")
        normalized_record["total_amount"] = extracted_data.get("total_amount")
        # Add logic to parse line items from extracted_data.get("line_items")

    # Further normalization or type conversion can happen here (e.g., str to float for amounts)

    return normalized_record

if __name__ == '__main__':
    # Example Usage
    invoice_data = {
        "vendor_name": "Google Inc.",
        "invoice_date": "2023-10-26",
        "total_amount": "150.75",
        "line_items": [
            {"description": "Cloud Services", "amount": "100.00"},
            {"description": "Support Fee", "amount": "50.75"}
        ]
    }
    normalized_invoice = normalize_expense(invoice_data, "invoice")
    print("Normalized Invoice:", json.dumps(normalized_invoice, indent=2))

    receipt_data = {
        "merchant_name": "Coffee Shop",
        "receipt_date": "2023-10-25",
        "tax_amount": "1.20",
        "total_amount": "12.00",
        "items": [
            {"description": "Coffee", "amount": "5.00"},
            {"description": "Sandwich", "amount": "5.80"}
        ]
    }
    normalized_receipt = normalize_expense(receipt_data, "receipt")
    print("Normalized Receipt:", json.dumps(normalized_receipt, indent=2))
