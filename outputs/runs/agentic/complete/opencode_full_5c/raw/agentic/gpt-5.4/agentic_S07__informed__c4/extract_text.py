from __future__ import annotations

from document_client import (
    DEFAULT_READ_MODEL,
    get_document_intelligence_client,
    resolve_model_id,
)
from document_models import DocumentRequest, TextExtractionResult


def extract_text(request: DocumentRequest) -> TextExtractionResult:
    client = get_document_intelligence_client()
    model_id = resolve_model_id(request.model_id, DEFAULT_READ_MODEL)
    poller = client.begin_analyze_document(
        model_id=model_id,
        body=request.document_bytes,
        content_type=request.mime_type,
    )
    result = poller.result()
    text = result.content or ""
    return TextExtractionResult(
        text=text,
        provider="azure-document-intelligence",
        raw=result,
    )
