from __future__ import annotations

from document_client import get_document_intelligence_client
from document_models import (
    DocumentSource,
    KeyValueExtractionResult,
    KeyValueField,
    load_binary,
    normalize_text,
)


def extract_key_values(source: DocumentSource) -> KeyValueExtractionResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        body=load_binary(source),
    )
    result = poller.result()
    fields = []
    for pair in result.key_value_pairs or []:
        key_text = normalize_text(pair.key.content if pair.key else "")
        value_text = normalize_text(pair.value.content if pair.value else "")
        page = None
        if pair.key and pair.key.bounding_regions:
            page = pair.key.bounding_regions[0].page_number
        fields.append(
            KeyValueField(
                key=key_text,
                value=value_text,
                confidence=getattr(pair, "confidence", None),
                page=page,
            )
        )
    return KeyValueExtractionResult(
        provider="azure-ai-documentintelligence", fields=fields, raw=result
    )
