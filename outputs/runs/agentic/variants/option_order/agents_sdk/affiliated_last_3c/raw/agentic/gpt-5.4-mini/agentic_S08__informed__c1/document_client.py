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


DEFAULT_INVOICE_MODEL_ID = "prebuilt-invoice"
DEFAULT_RECEIPT_MODEL_ID = "prebuilt-receipt"


def load_document_client_config(model_id: str) -> DocumentClientConfig:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    if not endpoint or not key:
        raise EnvironmentError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    return DocumentClientConfig(endpoint=endpoint, key=key, model_id=model_id)


def build_document_intelligence_client(config: Optional[DocumentClientConfig] = None) -> DocumentIntelligenceClient:
    config = config or load_document_client_config(DEFAULT_INVOICE_MODEL_ID)
    return DocumentIntelligenceClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key))


def normalize_currency_amount(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    try:
        return float(text)
    except ValueError:
        return None


def to_float_or_none(value: Any) -> Optional[float]:
    return normalize_currency_amount(value)


def confidence_value(value: Any) -> Optional[float]:
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def merge_non_empty(primary: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(fallback)
    for key, value in primary.items():
        if value not in (None, "", [], {}):
            merged[key] = value
    return merged
