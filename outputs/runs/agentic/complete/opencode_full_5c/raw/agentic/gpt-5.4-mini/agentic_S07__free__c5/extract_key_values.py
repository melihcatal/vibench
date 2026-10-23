from typing import Any, Dict
from document_client import get_client, load_image_bytes
from document_models import KeyValueRequest, normalize_key_value_result


def extract_key_values(image_path: str) -> Dict[str, Any]:
    client = get_client()
    payload = KeyValueRequest(image_bytes=load_image_bytes(image_path))
    result = client.extract_key_values(payload)
    return normalize_key_value_result(result).to_dict()
