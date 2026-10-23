from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import DocumentRequest


@dataclass
class DocumentClientConfig:
    endpoint: str
    key: str
    model_id: str = "prebuilt-read"

    @classmethod
    def from_env(cls) -> "DocumentClientConfig":
        endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
        key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
        model_id = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-read")
        if not endpoint or not key:
            raise EnvironmentError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
        return cls(endpoint=endpoint, key=key, model_id=model_id)


class DocumentServiceClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or DocumentClientConfig.from_env()
        self.client = DocumentIntelligenceClient(self.config.endpoint, AzureKeyCredential(self.config.key))

    def _open_document(self, request: DocumentRequest):
        request.validate()
        if request.document_bytes is not None:
            return request.document_bytes
        with open(request.document_path, "rb") as f:
            return f.read()

    def analyze(self, request: DocumentRequest, model_id: Optional[str] = None):
        document = self._open_document(request)
        model = model_id or self.config.model_id
        poller = self.client.begin_analyze_document(model, body=document)
        return poller.result()

    def raw_fields(self, result: Any) -> Dict[str, Any]:
        to_dict = getattr(result, "to_dict", None)
        return to_dict() if callable(to_dict) else {}
