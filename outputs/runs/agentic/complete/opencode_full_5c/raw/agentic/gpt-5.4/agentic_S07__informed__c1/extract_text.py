from __future__ import annotations

from document_client import get_document_intelligence_client
from document_models import (
    DocumentSource,
    TextExtractionResult,
    load_binary,
    normalize_text,
)


def extract_text(source: DocumentSource) -> TextExtractionResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body=load_binary(source),
        output_content_format="text",
    )
    result = poller.result()
    pages = []
    for page in result.pages or []:
        page_text = "\n".join(normalize_text(line.content) for line in page.lines or [])
        pages.append({"page_number": page.page_number, "text": page_text})
    return TextExtractionResult(
        provider="azure-ai-documentintelligence",
        text=normalize_text(result.content),
        pages=pages,
        raw=result,
    )
