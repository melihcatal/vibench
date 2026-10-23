from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_OCR_MODEL, get_document_client, read_bytes
from document_models import DocumentPage, OCRTextResponse, TextSpan, normalize_text


def extract_text(image_path: str) -> OCRTextResponse:
    client = get_document_client()
    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=DEFAULT_OCR_MODEL,
            body=AnalyzeDocumentRequest(bytes_source=f.read()),
        )
    result = poller.result()

    pages = [
        DocumentPage(
            page_number=page.page_number,
            width=page.width,
            height=page.height,
            unit=str(page.unit) if page.unit else None,
        )
        for page in (result.pages or [])
    ]

    spans = []
    for page in result.pages or []:
        for line in page.lines or []:
            polygon = [coord for point in (line.polygon or []) for coord in (point.x, point.y)] if line.polygon else []
            spans.append(
                TextSpan(
                    text=line.content,
                    page_number=page.page_number,
                    confidence=None,
                    polygon=polygon,
                )
            )

    return OCRTextResponse(
        text=normalize_text(result.content or ""),
        pages=pages,
        spans=spans,
        provider="azure-document-intelligence",
        model_id=DEFAULT_OCR_MODEL,
    )
