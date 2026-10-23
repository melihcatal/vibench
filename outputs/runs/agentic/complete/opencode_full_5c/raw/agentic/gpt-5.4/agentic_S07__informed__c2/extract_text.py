from __future__ import annotations

from document_client import get_document_intelligence_client, get_document_model_id
from document_models import (
    DocumentRequest,
    TextExtractionResult,
    TextPage,
    as_dict,
    normalize_text,
)


def extract_text(request: DocumentRequest) -> TextExtractionResult:
    client = get_document_intelligence_client()
    model_id = request.model_id or get_document_model_id("prebuilt-read")
    poller = client.begin_analyze_document(
        model_id=model_id,
        body=request.file_bytes,
        locale=request.locale,
        output_content_format="text",
    )
    result = poller.result()
    pages = [
        TextPage(
            page_number=page.page_number,
            text=normalize_text("\n".join(line.content for line in page.lines or [])),
            width=getattr(page, "width", None),
            height=getattr(page, "height", None),
        )
        for page in result.pages or []
    ]
    return TextExtractionResult(
        provider="azure-ai-documentintelligence",
        model_id=model_id,
        content=normalize_text(result.content),
        pages=pages,
        raw=as_dict(result),
    )
