from typing import Any, Dict
from document_client import get_client, load_image_bytes
from document_models import LayoutRequest, normalize_layout_result


def extract_layout(image_path: str) -> Dict[str, Any]:
    client = get_client()
    payload = LayoutRequest(image_bytes=load_image_bytes(image_path))
    result = client.extract_layout(payload)
    return normalize_layout_result(result).to_dict()
