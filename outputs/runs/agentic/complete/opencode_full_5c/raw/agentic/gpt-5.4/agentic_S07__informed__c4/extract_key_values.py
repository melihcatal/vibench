from __future__ import annotations

from document_client import (
    DEFAULT_KV_MODEL,
    get_document_intelligence_client,
    resolve_model_id,
)
from document_models import (
    DocumentRequest,
    KeyValueExtractionResult,
    KeyValueItem,
    normalize_text,
)


def extract_key_values(request: DocumentRequest) -> KeyValueExtractionResult:
    client = get_document_intelligence_client()
    model_id = resolve_model_id(request.model_id, DEFAULT_KV_MODEL)
    poller = client.begin_analyze_document(
        model_id=model_id,
        body=request.document_bytes,
        content_type=request.mime_type,
    )
    result = poller.result()
    items = []
    for pair in result.key_value_pairs or []:
        key_text = normalize_text(pair.key.content if pair.key else "")
        value_text = normalize_text(pair.value.content if pair.value else "")
        items.append(
            KeyValueItem(
                key=key_text,
                value=value_text,
                confidence=getattr(pair, "confidence", None),
            )
        )
    return KeyValueExtractionResult(
        provider="azure-document-intelligence",
        items=items,
        raw=result,
    )
