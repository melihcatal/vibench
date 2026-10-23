import os
from dataclasses import dataclass
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import DocumentInput


@dataclass
class DocumentClientConfig:
    endpoint: str
    key: str


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
        key=os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"],
    )


def create_client(
    config: Optional[DocumentClientConfig] = None,
) -> DocumentIntelligenceClient:
    cfg = config or load_config()
    return DocumentIntelligenceClient(
        endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key)
    )


def to_bytes(document: DocumentInput) -> bytes:
    return document.content_bytes
