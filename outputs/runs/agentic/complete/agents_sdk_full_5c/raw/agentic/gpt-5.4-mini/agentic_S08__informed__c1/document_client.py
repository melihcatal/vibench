from __future__ import annotations

import os
from typing import Any, Dict, Optional

from document_models import DocumentExtractionRequest, DocumentExtractionResponse

try:
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential
except Exception:  # pragma: no cover
    DocumentIntelligenceClient = None
    AzureKeyCredential = None


PROVIDER_NAME = "azure-ai-documentintelligence"


def load_document_intelligence_config() -> Dict[str, Optional[str]]:
    return {
        "endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        "key": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
    }


class StructuredDocumentClient:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        cfg = load_document_intelligence_config()
        self.endpoint = endpoint or cfg["endpoint"]
        self.key = key or cfg["key"]

    def _client(self):
        if DocumentIntelligenceClient is None or AzureKeyCredential is None:
            raise RuntimeError("azure-ai-documentintelligence is required")
        if not self.endpoint or not self.key:
            raise RuntimeError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
        return DocumentIntelligenceClient(self.endpoint, AzureKeyCredential(self.key))

    def analyze_invoice(self, request: DocumentExtractionRequest) -> DocumentExtractionResponse:
        client = self._client()
        result = client.begin_analyze_document("prebuilt-invoice", document=request.document_uri).result()
        return DocumentExtractionResponse(provider=PROVIDER_NAME, raw={"result": result})

    def analyze_receipt(self, request: DocumentExtractionRequest) -> DocumentExtractionResponse:
        client = self._client()
        result = client.begin_analyze_document("prebuilt-receipt", document=request.document_uri).result()
        return DocumentExtractionResponse(provider=PROVIDER_NAME, raw={"result": result})

    def analyze_custom(self, model_id: str, request: DocumentExtractionRequest) -> DocumentExtractionResponse:
        client = self._client()
        result = client.begin_analyze_document(model_id, document=request.document_uri).result()
        return DocumentExtractionResponse(provider=PROVIDER_NAME, raw={"result": result})


def response_payload(response: DocumentExtractionResponse) -> Dict[str, Any]:
    return {
        "provider": response.provider,
        "fields": {k: v.value for k, v in response.fields.items()},
        "line_items": [item.__dict__ for item in response.line_items],
        "raw": response.raw,
    }
