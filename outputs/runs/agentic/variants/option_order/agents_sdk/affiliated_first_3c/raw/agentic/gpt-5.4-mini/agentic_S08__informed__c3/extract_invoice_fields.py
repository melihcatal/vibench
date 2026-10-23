from __future__ import annotations

from typing import Any, Dict

from document_client import run_prebuilt_model
from document_models import ExtractionRequest, ensure_text, coerce_float, normalize_line_items

AZURE_INVOICE_MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(document_bytes: bytes, content_type: str = "application/pdf") -> Dict[str, Any]:
    request = ExtractionRequest(document_bytes=document_bytes, content_type=content_type)
    response = run_prebuilt_model(AZURE_INVOICE_MODEL_ID, request)
    raw = response.raw
    fields = getattr(raw, "documents", [])
    if fields:
        doc = fields[0]
        invoice = getattr(doc, "fields", {})
        line_items = invoice.get("Items", {}).get("value_array", []) if isinstance(invoice, dict) else []
        return {
            "vendor": ensure_text(invoice.get("VendorName", {}).get("value_string") if isinstance(invoice, dict) else None),
            "date": ensure_text(invoice.get("InvoiceDate", {}).get("value_date") if isinstance(invoice, dict) else None),
            "total": coerce_float(invoice.get("InvoiceTotal", {}).get("value_currency", {}).get("amount") if isinstance(invoice, dict) else None),
            "items": normalize_line_items(line_items),
            "provider": response.provider,
        }
    return {"vendor": "", "date": "", "total": 0.0, "items": [], "provider": response.provider}
