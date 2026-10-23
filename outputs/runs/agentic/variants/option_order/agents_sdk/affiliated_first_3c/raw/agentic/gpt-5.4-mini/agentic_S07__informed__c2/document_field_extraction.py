from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

PROVIDER = "azure-document-intelligence"
MODEL_ID = "prebuilt-invoice"


def document_field_extraction(source_url: str, endpoint: str, key: str) -> Dict[str, Any]:
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.begin_analyze_document(model_id=MODEL_ID, analyze_request=AnalyzeDocumentRequest(url_source=source_url))
    result = poller.result()
    fields = getattr(result, "documents", []) or []
    extracted: Dict[str, Any] = {}
    for doc in fields:
        for name, field in (getattr(doc, "fields", {}) or {}).items():
            extracted[name] = getattr(field, "value", None)
    return {"provider": PROVIDER, "model_id": MODEL_ID, "fields": extracted}
