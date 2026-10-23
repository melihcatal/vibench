from __future__ import annotations

from typing import Any, Dict, Optional

from document_client import DEFAULT_MODEL_ID, build_document_analysis_client
from document_models import OCRRequest, OCRResponse, normalize_document_text

AZURE_PREBUILT_READ_MODEL = DEFAULT_MODEL_ID


def extract_text(image_bytes: bytes, request: Optional[OCRRequest] = None) -> OCRResponse:
    req = request or OCRRequest(model_id=AZURE_PREBUILT_READ_MODEL)
    client = build_document_analysis_client()
    poller = client.begin_analyze_document(req.model_id, document=image_bytes)
    result = poller.result()

    lines = []
    pages = []
    for page in getattr(result, "pages", []) or []:
        page_lines = []
        for line in getattr(page, "lines", []) or []:
            page_lines.append({"content": line.content, "polygon": getattr(line, "polygon", None)})
            lines.append(line.content)
        pages.append({"page_number": page.page_number, "lines": page_lines})

    text = normalize_document_text("\n".join(lines))
    return OCRResponse(text=text, pages=pages, raw=getattr(result, "to_dict", lambda: None)())
