from typing import Dict
from document_client import get_document_client

def extract_key_values_from_url(document_url: str) -> Dict[str, str]:
    """
    Extracts key-value pairs from a form-like document at a given URL.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        A dictionary of extracted key-value pairs.
    """
    document_client = get_document_client()

    poller = document_client.begin_analyze_document(
        "prebuilt-document", {"urlSource": document_url}
    )
    result = poller.result()

    key_value_pairs = {}
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                key_value_pairs[kv_pair.key.content] = kv_pair.value.content
            elif kv_pair.key:
                key_value_pairs[kv_pair.key.content] = ""

    return key_value_pairs
