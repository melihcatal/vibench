from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

DEFAULT_READ_MODEL = "prebuilt-read"
DEFAULT_LAYOUT_MODEL = "prebuilt-layout"
DEFAULT_DOCUMENT_MODEL = "prebuilt-document"
DEFAULT_INVOICE_MODEL = "prebuilt-invoice"


class DocumentClientConfig:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        key: Optional[str] = None,
    ) -> None:
        self.endpoint = endpoint or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = key or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        if not self.endpoint:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
        if not self.key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")


def get_document_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    config = DocumentClientConfig(endpoint=endpoint, key=key)
    return DocumentIntelligenceClient(
        endpoint=config.endpoint,
        credential=AzureKeyCredential(config.key),
    )


def load_document_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
