from __future__ import annotations

import os
from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_MODEL_ID = "prebuilt-invoice"


class AzureDocumentExtractionClient:
    def __init__(self, endpoint: str | None = None, api_key: str | None = None, model_id: str = DEFAULT_MODEL_ID):
        self.endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        self.model_id = model_id
        if not self.endpoint or not self.api_key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
        )

    def analyze_document_bytes(self, document_bytes: bytes, *, model_id: str | None = None) -> Any:
        poller = self.client.begin_analyze_document(
            model_id=model_id or self.model_id,
            body=document_bytes,
        )
        return poller.result()



def field_content(field: Any) -> Any:
    if field is None:
        return None
    for attr in ("value_string", "value_currency", "value_number", "value_date", "content", "value_array", "value_object"):
        if hasattr(field, attr):
            value = getattr(field, attr)
            if value is not None:
                return value
    return getattr(field, "content", None)



def field_confidence(field: Any) -> float | None:
    return getattr(field, "confidence", None)



def currency_value(field: Any) -> float | None:
    currency = getattr(field, "value_currency", None)
    if currency is None:
        return None
    return getattr(currency, "amount", None)



def parse_kv_fields(document: Any) -> Dict[str, Any]:
    docs = getattr(document, "documents", []) or []
    if not docs:
        return {}
    analyzed = docs[0]
    return getattr(analyzed, "fields", {}) or {}
