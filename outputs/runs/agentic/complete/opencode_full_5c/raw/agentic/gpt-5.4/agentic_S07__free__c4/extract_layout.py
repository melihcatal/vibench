from __future__ import annotations

from typing import List

from document_client import (
    build_process_request,
    document_to_dict,
    get_documentai_client,
    get_processor_name,
)
from document_models import (
    DocumentInput,
    LayoutElement,
    LayoutExtractionResult,
    normalize_polygon,
)


def extract_layout(
    document: DocumentInput, processor_id: str | None = None
) -> LayoutExtractionResult:
    client = get_documentai_client()
    request = build_process_request(
        document, get_processor_name(processor_id=processor_id)
    )
    response = client.process_document(request=request)
    processed = response.document
    elements: List[LayoutElement] = []
    for page_index, page in enumerate(processed.pages, start=1):
        for block in page.blocks:
            elements.append(
                LayoutElement(
                    element_type="block",
                    text=_layout_text(processed.text, block.layout.text_anchor),
                    page=page_index,
                    confidence=getattr(block.layout, "confidence", None),
                    bbox=normalize_polygon(
                        block.layout.bounding_poly.normalized_vertices
                    ),
                )
            )
        for line in page.lines:
            elements.append(
                LayoutElement(
                    element_type="line",
                    text=_layout_text(processed.text, line.layout.text_anchor),
                    page=page_index,
                    confidence=getattr(line.layout, "confidence", None),
                    bbox=normalize_polygon(
                        line.layout.bounding_poly.normalized_vertices
                    ),
                )
            )
        for table_index, table in enumerate(page.tables):
            elements.append(
                LayoutElement(
                    element_type="table",
                    text=_table_text(processed.text, table),
                    page=page_index,
                    bbox=normalize_polygon(
                        table.layout.bounding_poly.normalized_vertices
                    ),
                    metadata={"table_index": table_index},
                )
            )
    return LayoutExtractionResult(
        provider="google_document_ai",
        elements=elements,
        raw_response=document_to_dict(processed),
    )


def _layout_text(full_text: str, anchor) -> str:
    if not getattr(anchor, "text_segments", None):
        return ""
    parts = []
    for segment in anchor.text_segments:
        start = int(getattr(segment, "start_index", 0) or 0)
        end = int(segment.end_index)
        parts.append(full_text[start:end])
    return "".join(parts).strip()


def _table_text(full_text: str, table) -> str:
    rows = []
    for row in list(table.header_rows) + list(table.body_rows):
        rows.append(
            " | ".join(
                _layout_text(full_text, cell.layout.text_anchor) for cell in row.cells
            )
        )
    return "\n".join(part for part in rows if part)
