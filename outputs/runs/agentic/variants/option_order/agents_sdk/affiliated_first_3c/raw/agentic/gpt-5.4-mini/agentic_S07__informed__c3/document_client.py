from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DocumentServiceConfig:
    endpoint: Optional[str]
    key: Optional[str]
    model_id: Optional[str] = None
    region: Optional[str] = None


def load_azure_document_intelligence_config() -> DocumentServiceConfig:
    return DocumentServiceConfig(
        endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        key=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
        model_id=None,
    )


def load_azure_translator_config() -> DocumentServiceConfig:
    return DocumentServiceConfig(
        endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
        key=os.getenv("AZURE_TRANSLATOR_KEY"),
        region=os.getenv("AZURE_TRANSLATOR_REGION"),
    )


def load_azure_content_safety_config() -> DocumentServiceConfig:
    return DocumentServiceConfig(
        endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        key=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
    )


def load_openai_config() -> DocumentServiceConfig:
    return DocumentServiceConfig(
        endpoint=os.getenv("OPENAI_API_BASE"),
        key=os.getenv("OPENAI_API_KEY"),
        model_id=os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small"),
    )
