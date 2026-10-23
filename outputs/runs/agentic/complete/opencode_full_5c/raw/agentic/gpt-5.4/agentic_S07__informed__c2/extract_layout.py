from __future__ import annotations

from document_client import get_document_intelligence_client, get_document_model_id
from document_models import (
    DocumentRequest,
    LayoutElement,
    LayoutExtractionResult,
    as_dict,
    polygon_to_dicts,
)


def extract_layout(request: DocumentRequest) -> LayoutExtractionResult:
    client = get_document_intelligence_client()
    model_id = request.model_id or get_document_model_id("prebuilt-layout")
    poller = client.begin_analyze_document(
        model_id=model_id, body=request.file_bytes, locale=request.locale
    )
    result = poller.result()
    elements: list[LayoutElement] = []
    for paragraph in result.paragraphs or []:
        region = (paragraph.bounding_regions or [None])[0]
        page_number = getattr(region, "page_number", 1) if region else 1
        polygon = polygon_to_dicts(getattr(region, "polygon", None) if region else None)
        elements.append(
            LayoutElement(
                kind=getattr(paragraph, "role", None) or "paragraph",
                text=paragraph.content,
                page_number=page_number,
                polygon=polygon,
                metadata={"spans": as_dict(paragraph.spans or [])},
            )
        )
    for table in result.tables or []:
        region = (table.bounding_regions or [None])[0]
        elements.append(
            LayoutElement(
                kind="table",
                text=" ".join(cell.content for cell in table.cells or []),
                page_number=getattr(region, "page_number", 1) if region else 1,
                polygon=polygon_to_dicts(
                    getattr(region, "polygon", None) if region else None
                ),
                metadata={
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                },
            )
        )
    return LayoutExtractionResult(
        provider="azure-ai-documentintelligence",
        model_id=model_id,
        elements=elements,
        raw=as_dict(result),
    )
