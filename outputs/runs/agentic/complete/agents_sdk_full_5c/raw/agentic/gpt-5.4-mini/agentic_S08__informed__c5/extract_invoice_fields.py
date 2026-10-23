from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import DocumentExtractionConfig

INVOICE_MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(source_url: str) -> Dict[str, Any]:
    config = DocumentExtractionConfig.from_env()
    client = DocumentIntelligenceClient(config.endpoint, AzureKeyCredential(config.key))
    poller = client.begin_analyze_document(INVOICE_MODEL_ID, {"urlSource": source_url})
    result = poller.result()
    payload = result.to_dict() if hasattr(result, "to_dict") else result
    docs = payload.get("documents", []) if isinstance(payload, dict) else []
    return {"provider": "azure-document-intelligence", "model_id": INVOICE_MODEL_ID, "raw": payload, "documents": docs}
