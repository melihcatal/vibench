from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_azure_document_intelligence_config
from document_models import OCRRequest


def extract_document_fields(request: OCRRequest) -> dict:
    config = load_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key or ""))
    with open(request.document_path, "rb") as handle:
        poller = client.begin_analyze_document("prebuilt-invoice", body=handle, content_type="application/octet-stream")
    result = poller.result()
    fields = {}
    for name, field in getattr(result, "documents", [{}])[0].fields.items() if getattr(result, "documents", None) else []:
        fields[name] = getattr(field, "content", None) or getattr(field, "value", None)
    return {"service": "Azure Document Intelligence prebuilt invoice", "fields": fields, "raw": result}
