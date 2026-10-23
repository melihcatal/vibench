from typing import Any, Dict
from document_client import get_client, load_image_bytes
from document_models import TableRequest, normalize_table_result


def extract_tables(image_path: str) -> Dict[str, Any]:
    client = get_client()
    payload = TableRequest(image_bytes=load_image_bytes(image_path))
    result = client.extract_tables(payload)
    return normalize_table_result(result).to_dict()
