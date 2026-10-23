from typing import List
from document_client import get_document_intelligence_client
from document_models import KeyValuePair


def extract_key_values_from_document(file_path: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form-like document.
    """
    document_intelligence_client = get_document_intelligence_client()

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
            key = kv_pair.key.content if kv_pair.key else ""
            value = kv_pair.value.content if kv_pair.value else ""
            if key and value:
                key_value_pairs.append(
                    KeyValuePair(key=key, value=value, confidence=kv_pair.confidence)
                )

    return key_value_pairs
