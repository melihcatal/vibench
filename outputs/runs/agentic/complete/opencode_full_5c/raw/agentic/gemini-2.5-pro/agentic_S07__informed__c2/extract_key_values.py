from document_client import get_document_client
from document_models import ExtractedKeyValues, KeyValuePair


def extract_key_values_from_document(file_path: str) -> ExtractedKeyValues:
    """
    Extracts key-value pairs from a document.
    """
    document_intelligence_client = get_document_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-document",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    key_values = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key = kv_pair.key.content if kv_pair.key else ""
            value = kv_pair.value.content if kv_pair.value else ""
            key_values.append(
                KeyValuePair(
                    key=key,
                    value=value,
                    confidence=kv_pair.confidence,
                )
            )

    return ExtractedKeyValues(key_values=key_values)
