from document_client import get_document_intelligence_client
from document_models import DocumentExtractionResult


def extract_key_values_from_document(
    document_content: bytes, mime_type: str
) -> DocumentExtractionResult:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-document", document_content, content_type=mime_type
    )
    result = poller.result()

    key_values = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key_values.append(
                {
                    "key": kv_pair.key.content if kv_pair.key else None,
                    "value": kv_pair.value.content if kv_pair.value else None,
                    "confidence": kv_pair.confidence,
                }
            )

    return DocumentExtractionResult(key_values=key_values)
