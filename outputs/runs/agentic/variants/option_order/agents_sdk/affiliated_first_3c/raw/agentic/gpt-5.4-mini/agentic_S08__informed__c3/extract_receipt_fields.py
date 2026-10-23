from __future__ import annotations

from typing import Any, Dict

from document_client import run_prebuilt_model
from document_models import ExtractionRequest, ensure_text, coerce_float

AZURE_RECEIPT_MODEL_ID = "prebuilt-receipt"


def extract_receipt_fields(document_bytes: bytes, content_type: str = "application/pdf") -> Dict[str, Any]:
    request = ExtractionRequest(document_bytes=document_bytes, content_type=content_type)
    response = run_prebuilt_model(AZURE_RECEIPT_MODEL_ID, request)
    raw = response.raw
    documents = getattr(raw, "documents", [])
    if documents:
        doc = documents[0]
        receipt = getattr(doc, "fields", {})
        items = []
        if isinstance(receipt, dict):
            for item in receipt.get("Items", {}).get("value_array", []):
                value = getattr(item, "value_object", item)
                items.append({
                    "description": ensure_text(value.get("Description", {}).get("value_string") if isinstance(value, dict) else None),
                    "amount": coerce_float(value.get("Amount", {}).get("value_currency", {}).get("amount") if isinstance(value, dict) else None),
                })
        return {
            "merchant": ensure_text(receipt.get("MerchantName", {}).get("value_string") if isinstance(receipt, dict) else None),
            "tax": coerce_float(receipt.get("TotalTax", {}).get("value_currency", {}).get("amount") if isinstance(receipt, dict) else None),
            "total": coerce_float(receipt.get("Total", {}).get("value_currency", {}).get("amount") if isinstance(receipt, dict) else None),
            "items": items,
            "provider": response.provider,
        }
    return {"merchant": "", "tax": 0.0, "total": 0.0, "items": [], "provider": response.provider}
