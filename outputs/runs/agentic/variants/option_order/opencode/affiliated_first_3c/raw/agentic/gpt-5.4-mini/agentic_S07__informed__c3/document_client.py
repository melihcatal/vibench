import os
from dataclasses import dataclass

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_endpoint() -> str:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    if not endpoint:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
    return endpoint


def get_key() -> str:
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    if not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")
    return key


def build_client() -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(get_endpoint(), AzureKeyCredential(get_key()))


@dataclass
class DocumentServiceConfig:
    endpoint: str
    key: str


def load_config() -> DocumentServiceConfig:
    return DocumentServiceConfig(endpoint=get_endpoint(), key=get_key())
