import os
from dataclasses import dataclass
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass
class DocumentClientConfig:
    endpoint: str
    key: str


def load_document_client_config() -> DocumentClientConfig:
    endpoint = os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT', '').strip()
    key = os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_KEY', '').strip()
    if not endpoint or not key:
        raise ValueError('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required')
    return DocumentClientConfig(endpoint=endpoint, key=key)


def create_document_intelligence_client(config: Optional[DocumentClientConfig] = None) -> DocumentIntelligenceClient:
    cfg = config or load_document_client_config()
    return DocumentIntelligenceClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))


def normalize_text(value):
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()
