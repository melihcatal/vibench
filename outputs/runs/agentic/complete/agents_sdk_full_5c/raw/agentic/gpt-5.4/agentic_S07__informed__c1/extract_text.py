from __future__ import annotations

from typing import Any, Dict, List

from document_client import DEFAULT_READ_MODEL, get_document_intelligence_client, load_document_bytes
from document_models import join_lines, normalize_whitespace


def extract_text(document_path: str, locale: str | None = None) -> Dict[str, Any]:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_READ_MODEL,
        body=load_document_bytes(document_path),
        locale=locale,
    )
    result = poller.result()

    pages: List[Dict[str, Any]] = []
    text_lines: List[str] = []
    for page in result.pages or []:
        page_lines: List[str] = []
        for line in page.lines or []:
            content = normalize_whitespace(line.content or "")
            if content:
                page_lines.append(content)
                text_lines.append(content)
        pages.append({
            "page_number": page.page_number,
            "width": page.width,
            "height": page.height,
            "unit": page.unit,
            "text": join_lines(page_lines),
        })

    return {
        "provider": "azure-ai-documentintelligence",
        "model_id": DEFAULT_READ_MODEL,
        "content": join_lines(text_lines),
        "pages": pages,
    }
