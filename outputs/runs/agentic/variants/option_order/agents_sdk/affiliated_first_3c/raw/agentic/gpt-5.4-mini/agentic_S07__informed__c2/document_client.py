from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentServiceConfig:
    endpoint: str
    key: str
    model_id: str = "prebuilt-read"


def load_config() -> DocumentServiceConfig:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    model_id = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-read").strip() or "prebuilt-read"
    return DocumentServiceConfig(endpoint=endpoint, key=key, model_id=model_id)


def get_client(config: Optional[DocumentServiceConfig] = None) -> DocumentIntelligenceClient:
    cfg = config or load_config()
    if not cfg.endpoint or not cfg.key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    return DocumentIntelligenceClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))


def build_content_url(source_url: str) -> str:
    if not source_url:
        raise ValueError("source_url is required")
    return source_url.strip()
