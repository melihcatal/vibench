from typing import Any, Optional

from document_client import build_document_intelligence_client, coerce_document_bytes, default_polling_timeout
from document_models import LayoutResult, normalize_layout_result


def extract_layout(document: Any, *, endpoint: Optional[str] = None, key: Optional[str] = None) -> LayoutResult:
    client = build_document_intelligence_client(endpoint=endpoint, key=key)
    data = coerce_document_bytes(document)
    poller = client.begin_analyze_document("prebuilt-layout", data, content_type="application/octet-stream")
    result = poller.result(timeout=default_polling_timeout())
    return normalize_layout_result(result)
