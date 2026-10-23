import os
from typing import Any
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def load_endpoint(endpoint: str | None = None) -> str:
    value = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    if not value:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
    return value


def load_api_key(api_key: str | None = None) -> str:
    value = api_key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not value:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")
    return value


def build_azure_document_intelligence_client(endpoint: str | None = None, api_key: str | None = None) -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(endpoint=load_endpoint(endpoint), credential=AzureKeyCredential(load_api_key(api_key)))


def get_poller_result(poller: Any) -> Any:
    return poller.result()
