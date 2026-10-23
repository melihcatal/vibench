from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_API_VERSION = "2024-11-30"
DEFAULT_INVOICE_MODEL = "prebuilt-invoice"
DEFAULT_RECEIPT_MODEL = "prebuilt-receipt"


class DocumentAIConfig:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = DEFAULT_API_VERSION,
    ) -> None:
        self.endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        self.api_version = api_version
        if not self.endpoint or not self.api_key:
            raise ValueError(
                "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
            )


def get_document_client(config: Optional[DocumentAIConfig] = None) -> DocumentIntelligenceClient:
    cfg = config or DocumentAIConfig()
    return DocumentIntelligenceClient(
        endpoint=cfg.endpoint,
        credential=AzureKeyCredential(cfg.api_key),
        api_version=cfg.api_version,
    )


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def field_confidence(field) -> Optional[float]:
    return getattr(field, "confidence", None)


def field_value(field, default=None):
    if field is None:
        return default
    value = getattr(field, "value", None)
    if value is not None:
        return value
    content = getattr(field, "content", None)
    if content is not None:
        return content
    return default
