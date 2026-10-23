from typing import Dict, Any, Union
from pydantic import BaseModel
from document_models import NormalizedExpense, InvoiceFields, ReceiptFields


def normalize_expense(extracted_data: Dict[str, Any], doc_type: str) -> NormalizedExpense:
    if doc_type == "invoice":
        return _normalize_invoice(extracted_data)
    elif doc_type == "receipt":
        return _normalize_receipt(extracted_data)
    else:
        raise ValueError(f"Unsupported document type: {doc_type}")


def _normalize_invoice(data: Dict[str, Any]) -> NormalizedExpense:
    return NormalizedExpense(
        vendor=data.get("vendor"),
        date=data.get("date"),
        amount=float(data.get("total", 0)),
        currency="USD",  # Default, can be extracted if available
        items=[
            {
                "description": item.get("description"),
                "amount": float(item.get("total_price", 0)),
            }
            for item in data.get("line_items", [])
        ],
        document_type="invoice",
        confidence=data.get("confidence", 0.0),
    )


def _normalize_receipt(data: Dict[str, Any]) -> NormalizedExpense:
    return NormalizedExpense(
        vendor=data.get("merchant"),
        date=None,  # Receipts may not always have a date
        amount=float(data.get("total", 0)),
        currency="USD",  # Default, can be extracted if available
        items=[
            {
                "description": item.get("description"),
                "amount": float(item.get("price", 0)),
            }
            for item in data.get("items", [])
        ],
        document_type="receipt",
        confidence=data.get("confidence", 0.0),
    )