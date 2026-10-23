from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_OCR_MODEL = "prebuilt-read"
DEFAULT_LAYOUT_MODEL = "prebuilt-layout"
DEFAULT_KV_MODEL = "prebuilt-document"
DEFAULT_INVOICE_MODEL = "prebuilt-invoice"


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_document_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    endpoint = endpoint or get_env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    api_key = api_key or get_env("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
