from __future__ import annotations

from document_client import DEFAULT_LAYOUT_MODEL, create_document_client, read_bytes
from document_models import as_dict_list, normalize_key_value_pairs


def extract_key_values(file_path: str) -> dict:
    client = create_document_client()
    poller = client.begin_analyze_document(
        DEFAULT_LAYOUT_MODEL, body=read_bytes(file_path), features=["keyValuePairs"]
    )
    result = poller.result()
    pairs = normalize_key_value_pairs(result)
    return {
        "provider": "azure-document-intelligence",
        "model_id": DEFAULT_LAYOUT_MODEL,
        "key_value_pairs": as_dict_list(pairs),
    }
