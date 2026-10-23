from typing import List
from document_client import get_document_client
from document_models import DocumentKeyValuePair


def extract_key_value_pairs_from_document(file_path: str) -> List[DocumentKeyValuePair]:
    document_intelligence_client = get_document_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-document",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    key_value_pairs = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key_value_pairs.append(
                DocumentKeyValuePair(
                    key=kv_pair.key.content if kv_pair.key else "",
                    value=kv_pair.value.content if kv_pair.value else None,
                    confidence=kv_pair.confidence,
                )
            )
    return key_value_pairs
