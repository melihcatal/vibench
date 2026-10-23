from typing import Dict, Any, Optional
from document_models import NormalizedExpense, DocumentExtractionResponse
from document_client import get_firestore_client
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def normalize_expense(extracted_data: Dict[str, Any], document_type: str, config: Dict[str, Any] = None) -> NormalizedExpense:
    config = config or {}
    db = get_firestore_client()
    normalization_rules_ref = db.collection("normalization_rules").document(document_type)
    rules = normalization_rules_ref.get().to_dict()

    if not rules:
        logger.warning(f"No normalization rules found for document type: {document_type}. Using default normalization.")
        rules = {
            "vendor_name_map": {},
            "category_map": {}
        }

    normalized = NormalizedExpense()
    normalized.original_document_type = document_type
    normalized.extracted_data = extracted_data

    # Basic field mapping from extracted_data (could be invoice or receipt structure)
    if document_type == "invoice":
        vendor_raw = extracted_data.get("vendor", {}).get("value")
        date_raw = extracted_data.get("date", {}).get("value")
        total_raw = extracted_data.get("total", {}).get("value")
        line_items_raw = extracted_data.get("line_items", [])
        
        normalized.vendor_name = rules["vendor_name_map"].get(vendor_raw, vendor_raw)
        normalized.transaction_date = date_raw
        try:
            normalized.total_amount = float(total_raw) if total_raw else None
        except (ValueError, TypeError):
            logger.warning(f"Could not convert total_amount '{total_raw}' to float.")
            normalized.total_amount = None

        normalized.line_items = [{
            "description": item.get("description"),
            "quantity": item.get("quantity"),
            "amount": float(item.get("amount")) if item.get("amount") else None
        } for item in line_items_raw]
        normalized.currency = "USD" # Default currency
        normalized.category = rules["category_map"].get(normalized.vendor_name, "General Expense")

    elif document_type == "receipt":
        merchant_raw = extracted_data.get("merchant", {}).get("value")
        date_raw = extracted_data.get("date", {}).get("value")
        total_raw = extracted_data.get("total", {}).get("value")
        line_items_raw = extracted_data.get("line_items", [])

        normalized.vendor_name = rules["vendor_name_map"].get(merchant_raw, merchant_raw)
        normalized.transaction_date = date_raw
        try:
            normalized.total_amount = float(total_raw) if total_raw else None
        except (ValueError, TypeError):
            logger.warning(f"Could not convert total_amount '{total_raw}' to float.")
            normalized.total_amount = None

        normalized.line_items = [{
            "description": item.get("description"),
            "quantity": item.get("quantity"),
            "amount": float(item.get("amount")) if item.get("amount") else None
        } for item in line_items_raw]
        normalized.currency = "USD" # Default currency
        normalized.category = rules["category_map"].get(normalized.vendor_name, "General Expense")

    return normalized
