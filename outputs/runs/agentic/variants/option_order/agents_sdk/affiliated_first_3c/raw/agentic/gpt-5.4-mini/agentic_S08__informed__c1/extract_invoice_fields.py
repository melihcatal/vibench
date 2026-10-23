from __future__ import annotations

from typing import Any, Dict

from document_client import extract_document_fields
from document_models import DocumentExtractionResult, normalize_amount, normalize_text


def extract_invoice_fields(file_bytes: bytes) -> Dict[str, Any]:
    result: DocumentExtractionResult = extract_document_fields(file_bytes, model_id="prebuilt-invoice")
    return {
        "vendor": normalize_text(result.fields.get("VendorName", {}).value if hasattr(result.fields.get("VendorName", {}), "value") else getattr(result.fields.get("VendorName"), "value", None)),
        "date": normalize_text(result.fields.get("InvoiceDate", {}).value if hasattr(result.fields.get("InvoiceDate", {}), "value") else getattr(result.fields.get("InvoiceDate"), "value", None)),
        "total": normalize_amount(getattr(result.fields.get("InvoiceTotal"), "value", None)),
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "amount": item.amount,
                "confidence": item.confidence,
            }
            for item in result.line_items
        ],
        "provider": result.provider,
        "raw": result.raw,
    }
