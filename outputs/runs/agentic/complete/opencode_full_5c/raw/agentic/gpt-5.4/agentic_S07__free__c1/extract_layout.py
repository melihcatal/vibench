from __future__ import annotations

from typing import List

from document_client import (
    document_to_dict,
    process_document,
    text_from_layout,
    vertices_to_bbox,
)
from document_models import DocumentRequest, LayoutElement, LayoutResult


def extract_layout(request: DocumentRequest) -> LayoutResult:
    document = process_document(request, "GOOGLE_DOCUMENTAI_LAYOUT_PROCESSOR_ID")
    elements: List[LayoutElement] = []
    for page in document.pages:
        for block in page.blocks:
            elements.append(
                LayoutElement(
                    element_type="block",
                    text=text_from_layout(document, block.layout),
                    page=page.page_number,
                    confidence=float(block.layout.confidence or 0.0),
                    bbox=vertices_to_bbox(
                        block.layout.bounding_poly.normalized_vertices
                    ),
                )
            )
        for line in page.lines:
            elements.append(
                LayoutElement(
                    element_type="line",
                    text=text_from_layout(document, line.layout),
                    page=page.page_number,
                    confidence=float(line.layout.confidence or 0.0),
                    bbox=vertices_to_bbox(
                        line.layout.bounding_poly.normalized_vertices
                    ),
                )
            )
        for table in page.tables:
            elements.append(
                LayoutElement(
                    element_type="table",
                    text="",
                    page=page.page_number,
                    confidence=float(table.layout.confidence or 0.0),
                    bbox=vertices_to_bbox(
                        table.layout.bounding_poly.normalized_vertices
                    ),
                    metadata={
                        "header_rows": len(table.header_rows),
                        "body_rows": len(table.body_rows),
                    },
                )
            )
    return LayoutResult(elements=elements, provider_payload=document_to_dict(document))
