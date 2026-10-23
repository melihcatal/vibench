from typing import Dict, Any, Union
from pydantic import BaseModel
from document_models import InvoiceFields, ReceiptFields, NormalizedExpense


def normalize_expense(extracted_data: Union[InvoiceFields, ReceiptFields]) -> Dict[str, Any]:
    if isinstance(extracted_data, InvoiceFields):
        normalized = {
            "expense_type": "invoice",
            "vendor": extracted_data.vendor,
            "date": extracted_data.date,
            "amount": extracted_data.total,
            "line_items": extracted_data.line_items,
            "tax": None,
            "merchant": None
        }
    elif isinstance(extracted_data, ReceiptFields):
        normalized = {
            "expense_type": "receipt",
            "vendor": None,
            "date": None,
            "amount": extracted_data.total,
            "line_items": extracted_data.items,
            "tax": extracted_data.tax,
            "merchant": extracted_data.merchant
        }
    else:
        raise ValueError("Unsupported extracted data type")

    return NormalizedExpense(**normalized).dict()