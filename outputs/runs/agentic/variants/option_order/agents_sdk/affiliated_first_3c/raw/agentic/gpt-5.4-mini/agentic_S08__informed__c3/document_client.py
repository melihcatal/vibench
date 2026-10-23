from __future__ import annotations

import os
from typing import Any, Optional

from document_models import ExtractionRequest, ExtractionResponse

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")


def build_azure_document_intelligence_client() -> Any:
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    if not AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT or not AZURE_DOCUMENT_INTELLIGENCE_KEY:
        raise RuntimeError("Azure Document Intelligence credentials are required")
    return DocumentIntelligenceClient(
        endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY),
    )


def run_prebuilt_model(model_id: str, request: ExtractionRequest) -> ExtractionResponse:
    client = build_azure_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id,
        document=request.document_bytes,
        content_type=request.content_type,
        locale=request.locale,
    )
    result = poller.result()
    return ExtractionResponse(provider="azure-document-intelligence", fields={}, raw=result)
