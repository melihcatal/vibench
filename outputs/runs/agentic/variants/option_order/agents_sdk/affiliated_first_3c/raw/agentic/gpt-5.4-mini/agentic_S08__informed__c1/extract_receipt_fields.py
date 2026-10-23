from __future__ import annotations

from typing import Any, Dict

from document_client import build_azure_invoice_client
from document_models import DocumentExtractionResult, normalize_amount, normalize_text


def _parse_receipt_result(result: Any) -> DocumentExtractionResult:
    from document_client import parse_invoice_result

    parsed = parse_invoice_result(result)
    parsed.provider = "azure-document-intelligence-prebuilt-receipt"
    return parsed


def extract_receipt_fields(file_bytes: bytes) -> Dict[str, Any]:
    client = build_azure_invoice_client()
    poller = client.begin_analyze_document("prebuilt-receipt", body=file_bytes)
    result = _parse_receipt_result(poller.result())
    return {
        "merchant": normalize_text(getattr(result.fields.get("MerchantName"), "value", None)),
        "tax": normalize_amount(getattr(result.fields.get("TotalTax"), "value", None)),
        "total": normalize_amount(getattr(result.fields.get("Total"), "value", None)),
        "items": [
            {
                "description": item.description,
                "amount": item.amount,
                "confidence": item.confidence,
            }
            for item in result.line_items
        ],
        "provider": result.provider,
        "raw": result.raw,
    }
