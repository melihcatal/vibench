from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentServiceConfig:
    endpoint: str
    key: str
    model_id: str = "prebuilt-read"


@lru_cache(maxsize=1)
def load_config() -> DocumentServiceConfig:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    model_id = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-read").strip() or "prebuilt-read"
    return DocumentServiceConfig(endpoint=endpoint, key=key, model_id=model_id)


@lru_cache(maxsize=1)
def get_client() -> DocumentIntelligenceClient:
    config = load_config()
    if not config.endpoint or not config.key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    return DocumentIntelligenceClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key))


def normalize_source(source: bytes | bytearray | memoryview | str) -> bytes:
    if isinstance(source, (bytes, bytearray, memoryview)):
        return bytes(source)
    with open(source, "rb") as f:
        return f.read()


def content_to_text(result) -> str:
    content = getattr(result, "content", None)
    if content:
        return content
    pages = getattr(result, "pages", None) or []
    chunks: list[str] = []
    for page in pages:
        for line in getattr(page, "lines", []) or []:
            chunks.append(getattr(line, "content", ""))
    return "\n".join([c for c in chunks if c])
