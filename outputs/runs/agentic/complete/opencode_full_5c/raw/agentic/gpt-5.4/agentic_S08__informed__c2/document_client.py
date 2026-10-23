from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def create_document_intelligence_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    service_endpoint = endpoint or get_required_env(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
    )
    service_key = key or get_required_env("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(
        endpoint=service_endpoint, credential=AzureKeyCredential(service_key)
    )


def load_document_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as handle:
        return handle.read()
