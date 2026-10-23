from __future__ import annotations

from typing import List

from document_client import get_azure_document_client
from document_models import (
    DocumentInput,
    LayoutElement,
    LayoutResult,
    normalize_bbox,
    normalize_text,
)


def extract_layout(document: DocumentInput) -> LayoutResult:
    client = get_azure_document_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=document.source_bytes,
        content_type=document.mime_type,
    )
    result = poller.result()
    elements: List[LayoutElement] = []
    for page in result.pages or []:
        for line in page.lines or []:
            elements.append(
                LayoutElement(
                    element_type="line",
                    text=normalize_text(getattr(line, "content", "")),
                    page=page.page_number,
                    bbox=normalize_bbox(getattr(line, "polygon", None)),
                    metadata={"provider_model": "prebuilt-layout"},
                )
            )
    for table_index, table in enumerate(result.tables or []):
        page_number = (
            table.bounding_regions[0].page_number if table.bounding_regions else 1
        )
        elements.append(
            LayoutElement(
                element_type="table",
                text=f"table_{table_index + 1}",
                page=page_number,
                bbox=normalize_bbox(
                    table.bounding_regions[0].polygon
                    if table.bounding_regions
                    else None
                ),
                metadata={
                    "row_count": getattr(table, "row_count", 0),
                    "column_count": getattr(table, "column_count", 0),
                    "provider_model": "prebuilt-layout",
                },
            )
        )
    for paragraph in result.paragraphs or []:
        page_number = (
            paragraph.bounding_regions[0].page_number
            if paragraph.bounding_regions
            else 1
        )
        elements.append(
            LayoutElement(
                element_type=getattr(paragraph, "role", None) or "paragraph",
                text=normalize_text(getattr(paragraph, "content", "")),
                page=page_number,
                bbox=normalize_bbox(
                    paragraph.bounding_regions[0].polygon
                    if paragraph.bounding_regions
                    else None
                ),
                metadata={"provider_model": "prebuilt-layout"},
            )
        )
    return LayoutResult(
        provider="azure-document-intelligence",
        elements=elements,
        raw=result.as_dict(),
    )
