from document_models import ExtractedExpense, LineItem
from typing import Dict, Any

def normalize_expense(extracted_data: Dict[str, Any]) -> ExtractedExpense:
    """
    Normalizes extracted expense fields into a standard JSON schema.

    Args:
        extracted_data: A dictionary containing raw extracted fields from an invoice or receipt.

    Returns:
        An ExtractedExpense object with normalized fields.
    """
    normalized_fields = {
        "vendor_name": extracted_data.get("vendor_name") or extracted_data.get("merchant_name"),
        "document_date": extracted_data.get("invoice_date"), # Assuming invoice_date can be generic document_date
        "tax_amount": extracted_data.get("tax_amount"),
        "total_amount": extracted_data.get("total_amount"),
        "line_items": [],
        "additional_data": {}
    }

    # Normalize line items
    raw_line_items = extracted_data.get("line_items") or extracted_data.get("items", [])
    for item_data in raw_line_items:
        normalized_fields["line_items"].append(LineItem(**item_data))

    # Capture any other fields not explicitly mapped into additional_data
    for key, value in extracted_data.items():
        if key not in ["vendor_name", "merchant_name", "invoice_date", "tax_amount", "total_amount", "line_items", "items"]:
            normalized_fields["additional_data"][key] = value

    return ExtractedExpense(**normalized_fields)
