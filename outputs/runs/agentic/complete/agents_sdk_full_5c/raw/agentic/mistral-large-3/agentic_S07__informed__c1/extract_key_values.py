import os
from typing import List, Optional
from document_client import get_document_client
from document_models import KeyValuePair, KeyValueExtractionResponse


def extract_key_values(image_path: str, mime_type: Optional[str] = None) -> KeyValueExtractionResponse:
    """
    Extract key-value pairs from a form-like document using Azure AI Document Intelligence.
    """
    client = get_document_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        analyze_request=image_data,
        content_type="application/octet-stream"
    )
    result = poller.result()

    key_values = []
    for kv_pair in result.key_value_pairs:
        key_values.append(KeyValuePair(
            key=kv_pair.key.content if kv_pair.key else None,
            value=kv_pair.value.content if kv_pair.value else None,
            confidence=kv_pair.confidence
        ))

    return KeyValueExtractionResponse(key_values=key_values)