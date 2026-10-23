from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_KV_MODEL, get_document_client
from document_models import KeyValueItem, KeyValueResponse


def extract_key_values(document_path: str) -> KeyValueResponse:
    client = get_document_client()
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=DEFAULT_KV_MODEL,
            body=AnalyzeDocumentRequest(bytes_source=f.read()),
        )
    result = poller.result()

    pairs = []
    for item in result.key_value_pairs or []:
        key_text = item.key.content if item.key else ""
        value_text = item.value.content if item.value else ""
        page_number = None
        if item.key and item.key.bounding_regions:
            page_number = item.key.bounding_regions[0].page_number
        confidence = getattr(item, "confidence", None)
        pairs.append(KeyValueItem(key=key_text, value=value_text, page_number=page_number, confidence=confidence))

    return KeyValueResponse(pairs=pairs, provider="azure-document-intelligence", model_id=DEFAULT_KV_MODEL)
