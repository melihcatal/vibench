from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentClientConfig:
    endpoint: str
    key: str


@lru_cache(maxsize=1)
def load_config() -> DocumentClientConfig:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    if not endpoint or not key:
        raise EnvironmentError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
        )
    return DocumentClientConfig(endpoint=endpoint, key=key)


@lru_cache(maxsize=1)
def get_document_intelligence_client() -> DocumentIntelligenceClient:
    cfg = load_config()
    return DocumentIntelligenceClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))


def document_to_dict(result: Any) -> Dict[str, Any]:
    if hasattr(result, "to_dict"):
        return result.to_dict()
    if isinstance(result, dict):
        return result
    return {"result": result}


def field_value(field: Any) -> Optional[Any]:
    if field is None:
        return None
    for attr in ("value", "content", "text"):
        if hasattr(field, attr):
            value = getattr(field, attr)
            if value is not None:
                return value
    if isinstance(field, dict):
        for key in ("value", "content", "text"):
            if key in field and field[key] is not None:
                return field[key]
    return field
