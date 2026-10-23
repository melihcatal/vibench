from __future__ import annotations

from typing import Optional

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_READ_MODEL, get_document_client, load_document_bytes
from document_models import OCRTextResult, TextLine, normalize_text


def extract_text(document_path: str, model_id: str = DEFAULT_READ_MODEL, locale: Optional[str] = None) -> OCRTextResult:
    client = get_document_client()
    body = AnalyzeDocumentRequest(bytes_source=load_document_bytes(document_path))
    poller = client.begin_analyze_document(model_id=model_id, body=body, locale=locale)
    result = poller.result()

    lines = []
    full_text_parts = []
    for page in result.pages or []:
        for line in page.lines or []:
            content = getattr(line, "content", "") or ""
            full_text_parts.append(content)
            lines.append(
                TextLine(
                    content=content,
                    page_number=getattr(page, "page_number", None),
                    polygon=list(getattr(line, "polygon", []) or []),
                )
            )

    text = normalize_text("\n".join(full_text_parts) or (getattr(result, "content", "") or ""))
    return OCRTextResult(text=text, lines=lines, provider="azure-document-intelligence", model_id=model_id)
