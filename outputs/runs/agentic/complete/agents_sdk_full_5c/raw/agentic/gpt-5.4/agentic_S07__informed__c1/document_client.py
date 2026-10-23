from __future__ import annotations

import os
from typing import Optional

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


DEFAULT_API_VERSION = "2024-11-30"
DEFAULT_READ_MODEL = "prebuilt-read"
DEFAULT_LAYOUT_MODEL = "prebuilt-layout"
DEFAULT_INVOICE_MODEL = "prebuilt-invoice"


def require_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_document_intelligence_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    api_version: str = DEFAULT_API_VERSION,
) -> DocumentIntelligenceClient:
    service_endpoint = endpoint or require_env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    service_key = key or require_env("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(
        endpoint=service_endpoint,
        credential=AzureKeyCredential(service_key),
        api_version=api_version,
    )


def load_document_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
