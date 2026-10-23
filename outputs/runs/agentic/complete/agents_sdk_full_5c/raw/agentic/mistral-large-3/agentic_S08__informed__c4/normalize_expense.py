from typing import Dict, Any, Union
from pydantic import BaseModel
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse, NormalizedExpense


def normalize_expense(extracted_data: Union[InvoiceExtractionResponse, ReceiptExtractionResponse]) -> NormalizedExpense:
    """
    Normalizes extracted invoice or receipt fields into a standard JSON schema.
    """
    normalized = {
        "vendor_merchant": "",
        "transaction_date": "",
        "total_amount": 0.0,
        "tax_amount": 0.0,
        "items": [],
        "source_type": "unknown"
    }

    if isinstance(extracted_data, InvoiceExtractionResponse):
        normalized.update({
            "vendor_merchant": extracted_data.vendor,
            "transaction_date": extracted_data.date,
            "total_amount": float(extracted_data.total) if extracted_data.total else 0.0,
            "source_type": "invoice"
        })
        for item in extracted_data.line_items:
            normalized["items"].append({
                "description": item.description,
                "amount": float(item.amount) if item.amount else 0.0
            })

    elif isinstance(extracted_data, ReceiptExtractionResponse):
        normalized.update({
            "vendor_merchant": extracted_data.merchant,
            "transaction_date": "",  # Receipts may not always have a date in the same field
            "total_amount": float(extracted_data.total) if extracted_data.total else 0.0,
            "tax_amount": float(extracted_data.tax) if extracted_data.tax else 0.0,
            "source_type": "receipt"
        })
        for item in extracted_data.items:
            normalized["items"].append({
                "description": item.name,
                "amount": float(item.price) if item.price else 0.0
            })

    return NormalizedExpense(**normalized)