from __future__ import annotations

from document_client import DEFAULT_READ_MODEL, create_document_client, read_bytes
from document_models import as_dict_list, lines_to_text, normalize_ocr_lines


def extract_text(file_path: str) -> dict:
    client = create_document_client()
    poller = client.begin_analyze_document(
        DEFAULT_READ_MODEL, body=read_bytes(file_path)
    )
    result = poller.result()
    lines = normalize_ocr_lines(result)
    return {
        "provider": "azure-document-intelligence",
        "model_id": DEFAULT_READ_MODEL,
        "text": lines_to_text(lines),
        "lines": as_dict_list(lines),
    }
