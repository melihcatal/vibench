from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
DEFAULT_MODEL_ID = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-read")


@dataclass(frozen=True)
class DocumentClientConfig:
    endpoint: str = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    key: str = AZURE_DOCUMENT_INTELLIGENCE_KEY
    model_id: str = DEFAULT_MODEL_ID


def load_config(env: Optional[Dict[str, str]] = None) -> DocumentClientConfig:
    source = env or os.environ
    return DocumentClientConfig(
        endpoint=source.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
        key=source.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""),
        model_id=source.get("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-read"),
    )


def build_document_analysis_client(config: Optional[DocumentClientConfig] = None) -> DocumentAnalysisClient:
    cfg = config or load_config()
    if not cfg.endpoint or not cfg.key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    return DocumentAnalysisClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))
