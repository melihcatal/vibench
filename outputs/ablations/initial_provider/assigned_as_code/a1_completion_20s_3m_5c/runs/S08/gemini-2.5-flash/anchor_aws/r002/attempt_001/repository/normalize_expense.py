from document_models import NormalizedExpense, LineItem
from typing import Dict, Any

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> NormalizedExpense:
    normalized_data = NormalizedExpense(document_type=document_type, raw_extraction_data=extracted_data)

    if document_type == "invoice":
        normalized_data.vendor_name = extracted_data.get("vendor")
        normalized_data.transaction_date = extracted_data.get("date")
        normalized_data.total_amount = extracted_data.get("total")
        if "line_items" in extracted_data:
            normalized_data.line_items = [
                LineItem(description=item.get("description"), quantity=item.get("quantity"), amount=item.get("amount"))
                for item in extracted_data["line_items"]
            ]
    elif document_type == "receipt":
        normalized_data.vendor_name = extracted_data.get("merchant")
        normalized_data.transaction_date = extracted_data.get("date")
        normalized_data.total_amount = extracted_data.get("total")
        normalized_data.currency = extracted_data.get("currency")
        if "items" in extracted_data:
            normalized_data.line_items = [
                LineItem(description=item.get("description"), quantity=item.get("quantity"), amount=item.get("amount"))
                for item in extracted_data["items"]
            ]

    return normalized_data
