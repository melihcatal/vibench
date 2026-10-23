from __future__ import annotations

from document_client import get_azure_document_client
from document_models import DocumentInput, KeyValuePair, KeyValueResult, normalize_text


def extract_key_values(document: DocumentInput) -> KeyValueResult:
    client = get_azure_document_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        body=document.source_bytes,
        content_type=document.mime_type,
    )
    result = poller.result()
    pairs = []
    for pair in result.key_value_pairs or []:
        key_text = normalize_text(getattr(getattr(pair, "key", None), "content", ""))
        value_text = normalize_text(
            getattr(getattr(pair, "value", None), "content", "")
        )
        page_number = None
        if getattr(pair, "key", None) and pair.key.bounding_regions:
            page_number = pair.key.bounding_regions[0].page_number
        pairs.append(
            KeyValuePair(
                key=key_text,
                value=value_text,
                confidence=getattr(pair, "confidence", None),
                page=page_number,
            )
        )
    return KeyValueResult(
        provider="azure-document-intelligence",
        pairs=pairs,
        raw=result.as_dict(),
    )
