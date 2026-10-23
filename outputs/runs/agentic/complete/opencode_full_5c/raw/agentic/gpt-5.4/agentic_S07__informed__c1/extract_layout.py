from __future__ import annotations

from document_client import get_document_intelligence_client
from document_models import (
    DocumentSource,
    LayoutElement,
    LayoutExtractionResult,
    load_binary,
    normalize_text,
    polygon_to_bbox,
)


def extract_layout(source: DocumentSource) -> LayoutExtractionResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=load_binary(source),
    )
    result = poller.result()
    elements = []
    for page in result.pages or []:
        for line in page.lines or []:
            elements.append(
                LayoutElement(
                    element_type="line",
                    text=normalize_text(line.content),
                    page=page.page_number,
                    confidence=getattr(line, "confidence", None),
                    bbox=polygon_to_bbox(getattr(line, "polygon", None)),
                )
            )
    for table in result.tables or []:
        elements.append(
            LayoutElement(
                element_type="table",
                text=" ".join(
                    normalize_text(cell.content) for cell in table.cells or []
                ),
                page=(table.bounding_regions or [None])[0].page_number
                if table.bounding_regions
                else 1,
                bbox=polygon_to_bbox(
                    (table.bounding_regions or [None])[0].polygon
                    if table.bounding_regions
                    else None
                ),
                metadata={
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                },
            )
        )
    return LayoutExtractionResult(
        provider="azure-ai-documentintelligence", elements=elements, raw=result
    )
