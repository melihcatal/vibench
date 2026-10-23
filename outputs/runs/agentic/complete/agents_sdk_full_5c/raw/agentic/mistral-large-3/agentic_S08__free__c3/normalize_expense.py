from typing import Dict, Any, Union
from pydantic import BaseModel
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse, NormalizedExpense


def normalize_expense(extracted_data: Union[InvoiceExtractionResponse, ReceiptExtractionResponse]) -> NormalizedExpense:
    if isinstance(extracted_data, InvoiceExtractionResponse):
        return NormalizedExpense(
            vendor=extracted_data.vendor,
            date=extracted_data.date,
            amount=extracted_data.total,
            category="Invoice",
            items=extracted_data.line_items,
            tax=0.0  # Default, override if available
        )
    elif isinstance(extracted_data, ReceiptExtractionResponse):
        return NormalizedExpense(
            vendor=extracted_data.merchant,
            date="",  # Receipts may not have a date in the same format
            amount=extracted_data.total,
            category="Receipt",
            items=extracted_data.items,
            tax=extracted_data.tax
        )
    else:
        raise ValueError("Unsupported extraction type")