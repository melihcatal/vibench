from typing import List
from document_client import get_document_client
from document_models import KeyValuePair


def extract_key_values_from_url(document_url: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a document at a given URL.
    Uses Azure AI Document Intelligence's "prebuilt-document" model.
    """
    document_analysis_client = get_document_client()

    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-document", document_url
    )
    result = poller.result()

    extracted_pairs = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                extracted_pairs.append(
                    KeyValuePair(
                        key=kv_pair.key.content,
                        value=kv_pair.value.content,
                        confidence=kv_pair.confidence,
                    )
                )
    return extracted_pairs
