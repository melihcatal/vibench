from document_client import get_document_intelligence_client, get_prebuilt_model_id
from document_models import KeyValueExtractionResult


def extract_key_values(file_path: str) -> KeyValueExtractionResult:
    client = get_document_intelligence_client()
    with open(file_path, "rb") as stream:
        poller = client.begin_analyze_document(
            get_prebuilt_model_id("key_values"), body=stream
        )
    result = poller.result()
    pairs = []
    for kv in getattr(result, "key_values", []) or []:
        key = getattr(getattr(kv, "key", None), "content", None)
        value = getattr(getattr(kv, "value", None), "content", None)
        pairs.append({"key": key, "value": value})
    return KeyValueExtractionResult(pairs=pairs)
