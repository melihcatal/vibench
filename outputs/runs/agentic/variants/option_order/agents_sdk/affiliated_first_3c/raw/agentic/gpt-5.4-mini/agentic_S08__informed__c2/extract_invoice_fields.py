from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, response_from_result
from document_models import ExtractionRequest

MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(source_uri: str) -> Dict[str, Any]:
    client = build_client()
    result = client.begin_analyze_document(MODEL_ID, AnalyzeDocumentRequest(url_source=source_uri)).result()
    response = response_from_result(result, provider="azure-document-intelligence")
    return {
        "vendor": response.fields.get("VendorName") or response.fields.get("vendor"),
        "date": response.fields.get("InvoiceDate") or response.fields.get("date"),
        "total": response.fields.get("InvoiceTotal") or response.fields.get("total"),
        "line_items": [item.__dict__ for item in response.line_items],
        "provider": response.provider,
    }
