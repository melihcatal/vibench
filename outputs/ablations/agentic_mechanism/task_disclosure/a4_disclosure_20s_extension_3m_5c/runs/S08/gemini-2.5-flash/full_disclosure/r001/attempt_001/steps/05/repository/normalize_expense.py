import json

def normalize_expense_fields(extracted_fields: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema.

    Args:
        extracted_fields: A dictionary containing the extracted fields from an expense document.

    Returns:
        A dictionary representing the normalized expense record.
    """
    # Using a schema inspired by Google Cloud Document AI's general document processor output structure
    # This is a placeholder for a more complex integration if specific Document AI processors were used.
    normalized_schema = {
        "document_type": extracted_fields.get("document_type", "expense_record"),
        "vendor_name": extracted_fields.get("vendor_name"),
        "transaction_date": extracted_fields.get("transaction_date"),
        "total_amount": extracted_fields.get("total_amount"),
        "currency": extracted_fields.get("currency"),
        "line_items": extracted_fields.get("line_items", []),
        "tax_amount": extracted_fields.get("tax_amount"),
        "merchant_address": extracted_fields.get("merchant_address"),
        "payment_method": extracted_fields.get("payment_method"),
        "notes": extracted_fields.get("notes")
    }

    return {k: v for k, v in normalized_schema.items() if v is not None}
