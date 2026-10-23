from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_intelligence_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    service_endpoint = endpoint or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    service_key = key or os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    credential = AzureKeyCredential(service_key)
    return DocumentIntelligenceClient(endpoint=service_endpoint, credential=credential)


def require_confidence_threshold(default: float = 0.5) -> float:
    value = os.getenv("DOCUMENT_CONFIDENCE_THRESHOLD")
    return float(value) if value else default
