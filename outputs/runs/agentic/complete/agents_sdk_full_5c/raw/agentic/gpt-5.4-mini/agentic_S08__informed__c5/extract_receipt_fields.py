from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import DocumentExtractionConfig

RECEIPT_MODEL_ID = "prebuilt-receipt"


def extract_receipt_fields(source_url: str) -> Dict[str, Any]:
    config = DocumentExtractionConfig.from_env()
    client = DocumentIntelligenceClient(config.endpoint, AzureKeyCredential(config.key))
    poller = client.begin_analyze_document(RECEIPT_MODEL_ID, {"urlSource": source_url})
    result = poller.result()
    payload = result.to_dict() if hasattr(result, "to_dict") else result
    return {"provider": "azure-document-intelligence", "model_id": RECEIPT_MODEL_ID, "raw": payload}
