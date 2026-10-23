from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import DocumentRequest, DocumentSource


@dataclass
class DocumentClientConfig:
    endpoint: str
    key: str
    model_id: str = "prebuilt-read"
    invoice_model_id: str = "prebuilt-invoice"


def load_config() -> DocumentClientConfig:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    if not endpoint or not key:
        raise EnvironmentError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    return DocumentClientConfig(endpoint=endpoint, key=key)


def build_client(config: Optional[DocumentClientConfig] = None) -> DocumentIntelligenceClient:
    cfg = config or load_config()
    return DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))


def request_to_stream(request: DocumentRequest):
    if request.source.image_bytes is not None:
        return request.source.image_bytes
    if request.source.path:
        with open(request.source.path, "rb") as f:
            return f.read()
    if request.source.url:
        return request.source.url
    raise ValueError("DocumentRequest.source must define image_bytes, path, or url")


def choose_model(request: DocumentRequest, config: Optional[DocumentClientConfig] = None) -> str:
    cfg = config or load_config()
    if any(feature in {"key_values", "invoice", "fields"} for feature in request.features):
        return cfg.invoice_model_id
    return cfg.model_id
