from typing import Dict, Any, Union
from pydantic import BaseModel
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse, NormalizedExpense


def normalize_expense(extraction_result: Union[InvoiceExtractionResponse, ReceiptExtractionResponse]) -> NormalizedExpense:
    raw_fields = extraction_result.raw_fields
    normalized = {
        "vendor_merchant": raw_fields.get("vendor", raw_fields.get("merchant", "")),
        "date": raw_fields.get("date", ""),
        "total_amount": float(raw_fields.get("total", 0.0)),
        "tax_amount": float(raw_fields.get("tax", 0.0)),
        "items": []
    }

    if "line_items" in raw_fields:
        normalized["items"] = [
            {
                "description": item.get("description", ""),
                "amount": float(item.get("amount", 0.0)),
                "quantity": float(item.get("quantity", 1.0))
            }
            for item in raw_fields["line_items"]
        ]
    elif "items" in raw_fields:
        normalized["items"] = [
            {
                "description": item.get("description", ""),
                "amount": float(item.get("price", 0.0)),
                "quantity": 1.0
            }
            for item in raw_fields["items"]
        ]

    return NormalizedExpense(**normalized)