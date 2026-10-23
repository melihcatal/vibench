from __future__ import annotations

from document_client import DEFAULT_MODEL_READ, OCRClientFactory, load_bytes
from document_models import OCRTextResult


def extract_text(document_path: str) -> OCRTextResult:
    client = OCRClientFactory().create_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_MODEL_READ,
        body=load_bytes(document_path),
        content_type="application/octet-stream",
    )
    result = poller.result()
    pages = []
    for page in result.pages or []:
        pages.append(
            {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "unit": page.unit,
                "line_count": len(page.lines or []),
            }
        )
    return OCRTextResult(content=result.content or "", pages=pages, model_id=DEFAULT_MODEL_READ)
