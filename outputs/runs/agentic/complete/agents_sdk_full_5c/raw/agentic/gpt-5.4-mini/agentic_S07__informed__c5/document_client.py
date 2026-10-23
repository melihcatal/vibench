from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentClientConfig:
    endpoint: str
    key: str

    @classmethod
    def from_env(cls) -> "DocumentClientConfig":
        endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
        key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
        if not endpoint or not key:
            raise EnvironmentError(
                "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
            )
        return cls(endpoint=endpoint, key=key)


@lru_cache(maxsize=1)
def get_document_client() -> DocumentIntelligenceClient:
    cfg = DocumentClientConfig.from_env()
    return DocumentIntelligenceClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))


def load_document_bytes(source: Any) -> bytes:
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    if hasattr(source, "read"):
        data = source.read()
        return data if isinstance(data, bytes) else str(data).encode("utf-8")
    if isinstance(source, str):
        with open(source, "rb") as f:
            return f.read()
    raise TypeError(f"Unsupported document source type: {type(source)!r}")


def begin_analyze_document(model_id: str, document: Any, *, content_type: Optional[str] = None):
    client = get_document_client()
    data = load_document_bytes(document)
    kwargs = {}
    if content_type:
        kwargs["content_type"] = content_type
    return client.begin_analyze_document(model_id=model_id, body=data, **kwargs)
