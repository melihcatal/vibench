from __future__ import annotations

from document_client import DEFAULT_LAYOUT_MODEL, create_document_client, read_bytes
from document_models import as_dict_list, normalize_layout_elements


def extract_layout(file_path: str) -> dict:
    client = create_document_client()
    poller = client.begin_analyze_document(
        DEFAULT_LAYOUT_MODEL, body=read_bytes(file_path)
    )
    result = poller.result()
    elements = normalize_layout_elements(result)
    return {
        "provider": "azure-document-intelligence",
        "model_id": DEFAULT_LAYOUT_MODEL,
        "elements": as_dict_list(elements),
    }
