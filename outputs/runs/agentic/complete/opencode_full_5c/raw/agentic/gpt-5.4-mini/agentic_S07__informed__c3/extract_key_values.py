from typing import Any, Optional

from document_client import build_document_intelligence_client, coerce_document_bytes, default_polling_timeout
from document_models import KeyValueResult, normalize_key_value_result


def extract_key_values(document: Any, *, endpoint: Optional[str] = None, key: Optional[str] = None) -> KeyValueResult:
    client = build_document_intelligence_client(endpoint=endpoint, key=key)
    data = coerce_document_bytes(document)
    poller = client.begin_analyze_document("prebuilt-document", data, content_type="application/octet-stream")
    result = poller.result(timeout=default_polling_timeout())
    return normalize_key_value_result(result)
