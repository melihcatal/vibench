from __future__ import annotations

from document_client import get_document_intelligence_client, get_document_model_id
from document_models import (
    DocumentRequest,
    KeyValueExtractionResult,
    KeyValuePair,
    as_dict,
)


def extract_key_values(request: DocumentRequest) -> KeyValueExtractionResult:
    client = get_document_intelligence_client()
    model_id = request.model_id or get_document_model_id("prebuilt-document")
    poller = client.begin_analyze_document(
        model_id=model_id, body=request.file_bytes, locale=request.locale
    )
    result = poller.result()
    pairs: list[KeyValuePair] = []
    for item in result.key_value_pairs or []:
        page_number = None
        if item.key and item.key.bounding_regions:
            page_number = item.key.bounding_regions[0].page_number
        confidence = getattr(item, "confidence", None)
        pairs.append(
            KeyValuePair(
                key=item.key.content if item.key else "",
                value=item.value.content if item.value else "",
                confidence=confidence,
                page_number=page_number,
            )
        )
    return KeyValueExtractionResult(
        provider="azure-ai-documentintelligence",
        model_id=model_id,
        pairs=pairs,
        raw=as_dict(result),
    )
