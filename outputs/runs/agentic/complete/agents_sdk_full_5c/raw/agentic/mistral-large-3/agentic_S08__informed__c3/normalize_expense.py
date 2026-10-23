from typing import Dict, Any, Union
from document_models import InvoiceResponse, ReceiptResponse, NormalizedExpense


def normalize_expense(extracted_data: Union[InvoiceResponse, ReceiptResponse]) -> NormalizedExpense:
    """
    Normalizes extracted invoice or receipt fields into a standard JSON schema.
    """
    normalized: Dict[str, Any] = {
        "expense_type": "invoice" if isinstance(extracted_data, InvoiceResponse) else "receipt",
        "vendor_or_merchant": extracted_data.vendor if isinstance(extracted_data, InvoiceResponse) else extracted_data.merchant,
        "date": extracted_data.date if isinstance(extracted_data, InvoiceResponse) else "",
        "total_amount": extracted_data.total,
        "tax_amount": extracted_data.tax if isinstance(extracted_data, ReceiptResponse) else 0.0,
        "line_items": [],
        "confidence_score": extracted_data.confidence,
    }

    if isinstance(extracted_data, InvoiceResponse):
        normalized["line_items"] = [
            {
                "description": item.description,
                "amount": item.amount,
                "quantity": item.quantity,
            }
            for item in extracted_data.line_items
        ]
    else:
        normalized["line_items"] = [
            {
                "description": item.description,
                "amount": item.amount,
                "quantity": 1,
            }
            for item in extracted_data.items
        ]

    return NormalizedExpense(**normalized)