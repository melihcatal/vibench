from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_API_VERSION = "2024-11-30"
DEFAULT_MODEL_ID = "prebuilt-invoice"


def get_document_intelligence_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    service_endpoint = endpoint or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    service_key = key or os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=service_endpoint,
        credential=AzureKeyCredential(service_key),
        api_version=DEFAULT_API_VERSION,
    )


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def get_model_id(document_type: str) -> str:
    if document_type in {"invoice", "receipt"}:
        return DEFAULT_MODEL_ID
    return DEFAULT_MODEL_ID
