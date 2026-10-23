
from typing import List, Union
from document_client import get_document_client
from document_models import KeyValuePair

def extract_key_values_from_document(file_source: Union[bytes, str]) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a document image or URL using Azure AI Document Intelligence.

    Args:
        file_source: A byte string containing the document content, or a URL string.
    """
    client = get_document_client()
    
    poller_args = {}
    if isinstance(file_source, bytes):
        poller_args["analyze_request"] = file_source
        poller_args["content_type"] = "application/octet-stream"
    elif isinstance(file_source, str):
        poller_args["url_source"] = file_source
    else:
        raise TypeError("file_source must be bytes or a URL string.")

    poller = client.begin_analyze_document(
        "prebuilt-document",
        **poller_args
    )
    result = poller.result()

    key_value_pairs = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key_content = kv_pair.key.content if kv_pair.key else ""
            value_content = kv_pair.value.content if kv_pair.value else ""
            
            key_value_pairs.append(
                KeyValuePair(
                    key=key_content,
                    value=value_content,
                    confidence=kv_pair.confidence,
                )
            )
            
    return key_value_pairs
