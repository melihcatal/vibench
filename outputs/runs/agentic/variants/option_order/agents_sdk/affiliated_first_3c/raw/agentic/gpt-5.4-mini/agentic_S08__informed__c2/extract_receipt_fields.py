from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, response_from_result

MODEL_ID = "prebuilt-receipt"


def extract_receipt_fields(source_uri: str) -> Dict[str, Any]:
    client = build_client()
    result = client.begin_analyze_document(MODEL_ID, AnalyzeDocumentRequest(url_source=source_uri)).result()
    response = response_from_result(result, provider="azure-document-intelligence")
    return {
        "merchant": response.fields.get("MerchantName") or response.fields.get("merchant"),
        "tax": response.fields.get("TotalTax") or response.fields.get("tax"),
        "total": response.fields.get("Total") or response.fields.get("total"),
        "items": [item.__dict__ for item in response.line_items],
        "provider": response.provider,
    }
