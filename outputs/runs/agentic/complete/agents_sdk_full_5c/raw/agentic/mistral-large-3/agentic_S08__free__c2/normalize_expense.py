from typing import Dict, Any, Union
from pydantic import BaseModel
from document_models import InvoiceFields, ReceiptFields, NormalizedExpense


def normalize_expense(extracted_data: Union[InvoiceFields, ReceiptFields]) -> Dict[str, Any]:
    """Normalize extracted expense fields into a standard JSON schema."""
    if isinstance(extracted_data, InvoiceFields):
        normalized = {
            "expense_type": "invoice",
            "vendor": extracted_data.vendor,
            "date": extracted_data.date,
            "total_amount": extracted_data.total,
            "line_items": extracted_data.line_items,
            "tax_amount": None,
            "merchant": None
        }
    elif isinstance(extracted_data, ReceiptFields):
        normalized = {
            "expense_type": "receipt",
            "merchant": extracted_data.merchant,
            "date": None,
            "total_amount": extracted_data.total,
            "line_items": extracted_data.items,
            "tax_amount": extracted_data.tax,
            "vendor": None
        }
    else:
        raise ValueError("Unsupported extracted data type")

    return NormalizedExpense(**normalized).dict()