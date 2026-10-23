from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_READ_MODEL = "prebuilt-read"
DEFAULT_LAYOUT_MODEL = "prebuilt-layout"
DEFAULT_KV_MODEL = "prebuilt-document"
DEFAULT_INVOICE_MODEL = "prebuilt-invoice"


def get_document_intelligence_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    resolved_endpoint = endpoint or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    resolved_key = api_key or os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=resolved_endpoint,
        credential=AzureKeyCredential(resolved_key),
    )


def resolve_model_id(explicit_model: Optional[str], default_model: str) -> str:
    return explicit_model or default_model
