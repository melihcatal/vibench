from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentClientConfig:
    endpoint: str
    key: str
    model_id: str


def load_document_client_config(model_id: str) -> DocumentClientConfig:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    return DocumentClientConfig(endpoint=endpoint, key=key, model_id=model_id)


def build_document_intelligence_client() -> DocumentIntelligenceClient:
    config = load_document_client_config("prebuilt-invoice")
    return DocumentIntelligenceClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key))


def summarize_document_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "field_count": len(fields),
        "present_fields": sorted(fields.keys()),
    }


def confidence_or_default(value: Optional[float], default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
