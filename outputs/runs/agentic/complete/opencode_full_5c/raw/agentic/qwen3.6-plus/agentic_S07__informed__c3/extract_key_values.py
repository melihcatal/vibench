from document_client import get_azure_document_client, load_image_bytes
from document_models import KeyValue, KeyValueResult


def extract_key_values_from_image(image_path: str) -> list[KeyValueResult]:
    client = get_azure_document_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-document", body=image_bytes
    )
    result = poller.result()
    kv_results = []
    if result.key_value_pairs:
        for pair in result.key_value_pairs:
            key_text = pair.key.content if pair.key else ""
            value_text = pair.value.content if pair.value else ""
            confidence = pair.confidence or 0.0
            kv_results.append(
                KeyValueResult(
                    pairs=[
                        KeyValue(key=key_text, value=value_text, confidence=confidence)
                    ]
                )
            )
    return kv_results
