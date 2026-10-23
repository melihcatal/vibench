from __future__ import annotations

from document_client import content_to_text, get_client, normalize_source
from document_models import OCRRequest, OCRResponse, normalize_text


def extract_text(source: str) -> OCRResponse:
    client = get_client()
    request = OCRRequest(source=source)
    payload = normalize_source(request.source)
    poller = client.begin_analyze_document(model_id="prebuilt-read", body=payload)
    result = poller.result()
    text = normalize_text(content_to_text(result))
    return OCRResponse(text=text, raw=getattr(result, "as_dict", lambda: None)())
