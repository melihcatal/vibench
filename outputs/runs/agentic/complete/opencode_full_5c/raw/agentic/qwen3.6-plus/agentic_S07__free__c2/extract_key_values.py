from document_client import get_document_analysis_client, load_image_bytes
from document_models import KeyValueResult, normalize_kv_response


AZURE_KV_MODEL_ID = "prebuilt-document"


def extract_key_values_from_image(image_path: str) -> KeyValueResult:
    client = get_document_analysis_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(
        model_id=AZURE_KV_MODEL_ID, document=image_bytes
    )
    result = poller.result()
    return normalize_kv_response(result)


def extract_key_values_from_bytes(image_bytes: bytes) -> KeyValueResult:
    client = get_document_analysis_client()
    poller = client.begin_analyze_document(
        model_id=AZURE_KV_MODEL_ID, document=image_bytes
    )
    result = poller.result()
    return normalize_kv_response(result)


def get_kv_dict(kv_result: KeyValueResult) -> dict:
    return kv_result.to_dict()


def get_kv_by_key(kv_result: KeyValueResult, key: str) -> str:
    for kv in kv_result.key_values:
        if kv.key.lower() == key.lower():
            return kv.value
    return ""


def get_high_confidence_kvs(kv_result: KeyValueResult, threshold: float = 0.8) -> list:
    return [kv for kv in kv_result.key_values if kv.confidence >= threshold]
