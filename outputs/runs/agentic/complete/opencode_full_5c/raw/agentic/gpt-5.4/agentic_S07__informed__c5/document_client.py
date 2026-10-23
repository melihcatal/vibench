from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_READ_MODEL = "prebuilt-read"
DEFAULT_LAYOUT_MODEL = "prebuilt-layout"
DEFAULT_INVOICE_MODEL = "prebuilt-invoice"


def get_endpoint() -> str:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    return endpoint.rstrip("/")


def get_key() -> str:
    return os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]


def create_document_client(
    endpoint: Optional[str] = None, key: Optional[str] = None
) -> DocumentIntelligenceClient:
    service_endpoint = (endpoint or get_endpoint()).rstrip("/")
    service_key = key or get_key()
    return DocumentIntelligenceClient(
        endpoint=service_endpoint, credential=AzureKeyCredential(service_key)
    )


def read_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as handle:
        return handle.read()
