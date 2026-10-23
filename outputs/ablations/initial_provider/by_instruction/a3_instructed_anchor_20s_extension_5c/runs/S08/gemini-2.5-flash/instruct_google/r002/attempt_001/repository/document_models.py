from typing import List, Dict, Any, Optional

def create_normalized_expense_schema() -> Dict[str, Any]:
    """
    Returns a template for a normalized expense schema.
    """
    return {
        "document_type": None,  # "invoice" or "receipt"
        "vendor_info": {
            "name": None,
            "address": None,
            "phone": None,
        },
        "transaction_date": None,
        "total_amount": None,
        "currency": None,
        "tax_amount": None,
        "line_items": [],
        "notes": None,
        "raw_extraction_data": {},
        "confidence_scores": {},
    }

def create_line_item_schema() -> Dict[str, Any]:
    """
    Returns a template for a line item schema.
    """
    return {
        "description": None,
        "quantity": None,
        "unit_price": None,
        "total_price": None,
    }
