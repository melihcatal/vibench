from __future__ import annotations

from document_client import get_azure_document_client
from document_models import DocumentInput, OCRTextResult, normalize_text


def extract_text(document: DocumentInput) -> OCRTextResult:
    client = get_azure_document_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body=document.source_bytes,
        content_type=document.mime_type,
    )
    result = poller.result()
    pages = []
    page_texts = []
    for page in result.pages or []:
        lines = [
            normalize_text(getattr(line, "content", "")) for line in page.lines or []
        ]
        page_text = "\n".join(line for line in lines if line)
        page_texts.append(page_text)
        pages.append(
            {
                "page_number": page.page_number,
                "width": getattr(page, "width", None),
                "height": getattr(page, "height", None),
                "unit": getattr(page, "unit", None),
                "text": page_text,
            }
        )
    return OCRTextResult(
        provider="azure-document-intelligence",
        text="\n\n".join(part for part in page_texts if part),
        pages=pages,
        raw=result.as_dict(),
    )
