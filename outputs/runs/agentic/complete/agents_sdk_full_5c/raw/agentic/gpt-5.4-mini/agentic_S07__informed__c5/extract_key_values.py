from __future__ import annotations

from document_client import begin_analyze_document
from document_models import KeyValueResponse, normalize_key_values


def extract_key_values(document) -> KeyValueResponse:
    poller = begin_analyze_document("prebuilt-document", document, content_type="application/octet-stream")
    result = poller.result()
    return normalize_key_values(getattr(result, "key_value_pairs", []) or [])
