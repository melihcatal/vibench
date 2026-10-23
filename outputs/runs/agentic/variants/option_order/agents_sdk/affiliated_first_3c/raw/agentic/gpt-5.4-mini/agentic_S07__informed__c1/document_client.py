from __future__ import annotations

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
    model_id: str = "prebuilt-read"
    locale: Optional[str] = None


def load_config(model_id: Optional[str] = None, locale: Optional[str] = None) -> DocumentClientConfig:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentClientConfig(
        endpoint=endpoint,
        key=key,
        model_id=model_id or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-read"),
        locale=locale or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_LOCALE"),
    )


def build_client(config: Optional[DocumentClientConfig] = None) -> DocumentIntelligenceClient:
    cfg = config or load_config()
    return DocumentIntelligenceClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))


def as_document_input(content: bytes, content_type: str = "image/png", locale: Optional[str] = None, model: Optional[str] = None, filename: Optional[str] = None) -> DocumentInput:
    return DocumentInput(content=content, content_type=content_type, locale=locale, model=model, filename=filename)
