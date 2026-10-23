from document_client import get_document_intelligence_client
from document_models import ExtractedKeyValues
import io


def extract_key_values_from_document(document_content: bytes) -> ExtractedKeyValues:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-document", document_content, content_type="application/octet-stream"
    )
    result = poller.result()
    key_value_pairs = []
    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            key_value_pairs.append(
                {
                    "key_content": kvp.key.content,
                    "value_content": kvp.value.content if kvp.value else None,
                }
            )
    return ExtractedKeyValues(key_value_pairs=key_value_pairs)
