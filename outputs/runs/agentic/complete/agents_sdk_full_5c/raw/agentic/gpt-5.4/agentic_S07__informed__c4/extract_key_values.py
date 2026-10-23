from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_document_intelligence_client, guess_content_type, read_bytes
from document_models import KeyValueItem, KeyValueResult, normalize_text


def extract_key_values(document_path: str) -> KeyValueResult:
    client = get_document_intelligence_client()
    payload = read_bytes(document_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        body=AnalyzeDocumentRequest(bytes_source=payload),
        content_type=guess_content_type(document_path),
    )
    result = poller.result()

    items = []
    for pair in result.key_value_pairs or []:
        key_text = normalize_text(pair.key.content if pair.key else "")
        value_text = normalize_text(pair.value.content if pair.value else "")
        page_number = None
        if pair.key and pair.key.bounding_regions:
            page_number = pair.key.bounding_regions[0].page_number
        elif pair.value and pair.value.bounding_regions:
            page_number = pair.value.bounding_regions[0].page_number
        items.append(
            KeyValueItem(
                key=key_text,
                value=value_text,
                confidence=pair.confidence,
                page=page_number,
            )
        )

    return KeyValueResult(
        items=items,
        provider="azure-ai-documentintelligence:prebuilt-document",
        raw=result,
    )
