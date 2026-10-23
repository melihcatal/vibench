import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_endpoint() -> str:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    if not endpoint:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
    return endpoint


def get_key() -> str:
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")
    return key


def create_client() -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(get_endpoint(), AzureKeyCredential(get_key()))


def open_document(path: Optional[str] = None, data: Optional[bytes] = None) -> bytes:
    if data is not None:
        return data
    if not path:
        raise ValueError("document_path or document_bytes is required")
    with open(path, "rb") as handle:
        return handle.read()
