from __future__ import annotations

from document_client import DEFAULT_DOCUMENT_MODEL, ensure_bytes, get_document_intelligence_client
from document_models import OCRTextResult, flatten_azure_read_content


def extract_text(document_bytes: bytes, model_id: str = "prebuilt-read") -> OCRTextResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(model_id=model_id or DEFAULT_DOCUMENT_MODEL, body=ensure_bytes(document_bytes))
    result = poller.result()
    payload = result.as_dict()
    return OCRTextResult(
        provider="azure-document-intelligence",
        text=flatten_azure_read_content(payload),
        pages=payload.get("pages", []),
        raw=payload,
    )
