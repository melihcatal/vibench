import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentClientConfig:
    endpoint: str
    key: str


def load_config() -> DocumentClientConfig:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
        )
    return DocumentClientConfig(endpoint=endpoint, key=key)


@lru_cache(maxsize=1)
def get_client() -> DocumentIntelligenceClient:
    config = load_config()
    return DocumentIntelligenceClient(config.endpoint, AzureKeyCredential(config.key))


def open_document(source: str):
    if source.startswith(("http://", "https://")):
        return source
    return open(source, "rb")
