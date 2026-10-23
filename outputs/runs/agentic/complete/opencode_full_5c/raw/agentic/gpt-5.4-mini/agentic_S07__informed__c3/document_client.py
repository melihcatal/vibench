import os
from typing import Any, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def build_document_intelligence_client(*, endpoint: Optional[str] = None, key: Optional[str] = None) -> DocumentIntelligenceClient:
    endpoint = endpoint or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = key or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def coerce_document_bytes(document: Any) -> bytes:
    if isinstance(document, bytes):
        return document
    if isinstance(document, str):
        with open(document, "rb") as f:
            return f.read()
    if hasattr(document, "read"):
        return document.read()
    raise TypeError("document must be bytes, path, or file-like object")


def default_polling_timeout() -> int:
    value = os.environ.get("DOCUMENT_INTELLIGENCE_TIMEOUT_SECONDS", "120")
    return int(value)
