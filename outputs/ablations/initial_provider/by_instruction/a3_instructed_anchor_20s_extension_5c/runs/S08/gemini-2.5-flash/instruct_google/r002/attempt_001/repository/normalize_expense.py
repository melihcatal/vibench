from document_models import create_normalized_expense_schema, create_line_item_schema
from typing import Dict, Any

def normalize_invoice_fields(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes extracted invoice fields into a standard expense schema.
    """
    normalized_expense = create_normalized_expense_schema()
    normalized_expense["document_type"] = "invoice"
    normalized_expense["raw_extraction_data"] = invoice_data

    if invoice_data.get("vendor_name"):
        normalized_expense["vendor_info"]["name"] = invoice_data["vendor_name"]
    if invoice_data.get("invoice_date"):
        normalized_expense["transaction_date"] = invoice_data["invoice_date"]
    if invoice_data.get("total_amount"):
        normalized_expense["total_amount"] = invoice_data["total_amount"]
    
    for item in invoice_data.get("line_items", []):
        line_item = create_line_item_schema()
        line_item["description"] = item.get("description")
        line_item["total_price"] = item.get("amount")
        normalized_expense["line_items"].append(line_item)

    return normalized_expense

def normalize_receipt_fields(receipt_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes extracted receipt fields into a standard expense schema.
    """
    normalized_expense = create_normalized_expense_schema()
    normalized_expense["document_type"] = "receipt"
    normalized_expense["raw_extraction_data"] = receipt_data

    if receipt_data.get("merchant_name"):
        normalized_expense["vendor_info"]["name"] = receipt_data["merchant_name"]
    if receipt_data.get("total_amount"):
        normalized_expense["total_amount"] = receipt_data["total_amount"]
    if receipt_data.get("tax_amount"):
        normalized_expense["tax_amount"] = receipt_data["tax_amount"]
    
    for item in receipt_data.get("items", []):
        line_item = create_line_item_schema()
        line_item["description"] = item.get("description")
        line_item["total_price"] = item.get("total_price")
        normalized_expense["line_items"].append(line_item)

    return normalized_expense
