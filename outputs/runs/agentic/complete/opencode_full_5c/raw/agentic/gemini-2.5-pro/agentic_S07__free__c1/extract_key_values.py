from typing import List
from document_client import get_document_intelligence_client
from document_models import KeyValuePair, KeyValue, Span


def extract_key_values(image_path: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a document image.
    """
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-document",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    kv_pairs = []
    if result.documents:
        for document in result.documents:
            if not document.fields:
                continue
            for name, field in document.fields.items():
                key = KeyValue(
                    content=field.key.content,
                    spans=[
                        Span(offset=s.offset, length=s.length) for s in field.key.spans
                    ],
                )
                value = None
                if field.value:
                    value = KeyValue(
                        content=field.value,  # field.value is just a string, not an object with a content property
                        spans=[
                            Span(offset=s.offset, length=s.length) for s in field.spans
                        ],
                    )

                kv_pairs.append(
                    KeyValuePair(key=key, value=value, confidence=field.confidence)
                )

    return kv_pairs
