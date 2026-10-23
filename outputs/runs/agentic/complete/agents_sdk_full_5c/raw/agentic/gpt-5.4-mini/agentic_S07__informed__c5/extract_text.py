from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import begin_analyze_document
from document_models import OCRTextResponse, normalize_lines


def extract_text(document) -> OCRTextResponse:
    poller = begin_analyze_document("prebuilt-read", document, content_type="application/octet-stream")
    result = poller.result()
    lines = []
    pages = []
    for page in getattr(result, "pages", []) or []:
        pages.append({"page_number": getattr(page, "page_number", None), "width": getattr(page, "width", None), "height": getattr(page, "height", None)})
        lines.extend(getattr(page, "lines", []) or [])
    if not lines:
        lines = getattr(result, "paragraphs", []) or []
    return OCRTextResponse(text="\n".join(normalize_lines(lines)), pages=pages)
