from __future__ import annotations

from document_client import (
    DEFAULT_LAYOUT_MODEL,
    get_document_intelligence_client,
    resolve_model_id,
)
from document_models import (
    DocumentRequest,
    LayoutElement,
    LayoutExtractionResult,
    normalize_polygon,
    normalize_text,
)


def extract_layout(request: DocumentRequest) -> LayoutExtractionResult:
    client = get_document_intelligence_client()
    model_id = resolve_model_id(request.model_id, DEFAULT_LAYOUT_MODEL)
    poller = client.begin_analyze_document(
        model_id=model_id,
        body=request.document_bytes,
        content_type=request.mime_type,
    )
    result = poller.result()
    elements = []
    for page in result.pages or []:
        for line in page.lines or []:
            elements.append(
                LayoutElement(
                    kind="line",
                    text=normalize_text(line.content),
                    page=page.page_number,
                    bounding_polygon=normalize_polygon(line.polygon),
                )
            )
        for word in page.words or []:
            elements.append(
                LayoutElement(
                    kind="word",
                    text=normalize_text(word.content),
                    page=page.page_number,
                    bounding_polygon=normalize_polygon(word.polygon),
                    confidence=getattr(word, "confidence", None),
                )
            )
    for table in result.tables or []:
        elements.append(
            LayoutElement(
                kind="table",
                text=" ".join(
                    normalize_text(cell.content) for cell in table.cells or []
                ),
                page=(
                    table.bounding_regions[0].page_number
                    if table.bounding_regions
                    else 1
                ),
                bounding_polygon=normalize_polygon(
                    table.bounding_regions[0].polygon if table.bounding_regions else []
                ),
            )
        )
    return LayoutExtractionResult(
        text=result.content or "",
        provider="azure-document-intelligence",
        elements=elements,
        raw=result,
    )
