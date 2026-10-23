from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_MODEL_READ = "prebuilt-read"
DEFAULT_MODEL_LAYOUT = "prebuilt-layout"
DEFAULT_MODEL_DOCUMENT = "prebuilt-document"
DEFAULT_MODEL_INVOICE = "prebuilt-invoice"


class DocumentServiceConfig:
    def __init__(self) -> None:
        self.endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
        self.key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
        self.api_version = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION")


class OCRClientFactory:
    def __init__(self, config: Optional[DocumentServiceConfig] = None) -> None:
        self.config = config or DocumentServiceConfig()

    def create_client(self) -> DocumentIntelligenceClient:
        kwargs = {}
        if self.config.api_version:
            kwargs["api_version"] = self.config.api_version
        return DocumentIntelligenceClient(
            endpoint=self.config.endpoint,
            credential=AzureKeyCredential(self.config.key),
            **kwargs,
        )


def load_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
