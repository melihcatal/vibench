import os
from dataclasses import dataclass
from typing import Optional

from document_models import DocumentInput, build_image_source


@dataclass
class ClientConfig:
    azure_endpoint: str
    azure_api_key: str
    azure_api_version: str = "2024-02-29-preview"
    document_intelligence_model: str = "prebuilt-read"


class AzureDocumentClient:
    def __init__(self, config: Optional[ClientConfig] = None):
        self.config = config or ClientConfig(
            azure_endpoint=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
            azure_api_key=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_KEY", ""),
        )

    def _require_config(self) -> ClientConfig:
        if not self.config.azure_endpoint or not self.config.azure_api_key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_API_KEY are required")
        return self.config

    def _client(self):
        cfg = self._require_config()
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential

        return DocumentIntelligenceClient(cfg.azure_endpoint, AzureKeyCredential(cfg.azure_api_key))

    def analyze(self, document: DocumentInput, model_id: Optional[str] = None):
        cfg = self._require_config()
        client = self._client()
        source = build_image_source(document)
        model = model_id or cfg.document_intelligence_model
        poller = client.begin_analyze_document(model, source, content_type=document.content_type or "application/octet-stream")
        return poller.result()
