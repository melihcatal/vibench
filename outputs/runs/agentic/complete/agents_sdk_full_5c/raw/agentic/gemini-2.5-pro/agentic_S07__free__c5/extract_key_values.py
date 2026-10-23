# extract_key_values.py
from typing import List
from document_client import get_document_intelligence_client
from document_models import ExtractedKeyValuePair

def extract_key_values_from_url(document_url: str) -> List[ExtractedKeyValuePair]:
    """
    Extracts key-value pairs from a form-like document image using
    Azure AI Document Intelligence's "prebuilt-document" model.
    """
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-document", analyze_request={"urlSource": document_url}
    )
    result = poller.result()

    extracted_pairs: List[ExtractedKeyValuePair] = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                extracted_pairs.append(
                    ExtractedKeyValuePair(
                        key=kv_pair.key.content,
                        value=kv_pair.value.content,
                        confidence=kv_pair.confidence,
                    )
                )

    return extracted_pairs
