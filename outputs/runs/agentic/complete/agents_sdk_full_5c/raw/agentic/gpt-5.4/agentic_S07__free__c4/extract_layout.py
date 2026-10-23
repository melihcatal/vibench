from __future__ import annotations

from typing import List

from document_client import process_document_bytes
from document_models import LayoutElement, get_text_from_anchor, normalize_vertices


DEFAULT_MIME_TYPE = "image/png"


def extract_layout(file_path: str, mime_type: str = DEFAULT_MIME_TYPE) -> List[LayoutElement]:
    with open(file_path, "rb") as f:
        result = process_document_bytes(f.read(), mime_type)
    document = result.document
    elements: List[LayoutElement] = []
    for page in document.pages:
        for block in page.blocks:
            elements.append(
                LayoutElement(
                    element_type="block",
                    text=get_text_from_anchor(document, block.layout.text_anchor),
                    page=page.page_number,
                    bbox=normalize_vertices(block.layout.bounding_poly.normalized_vertices),
                    confidence=getattr(block.layout, "confidence", None),
                )
            )
        for line in page.lines:
            elements.append(
                LayoutElement(
                    element_type="line",
                    text=get_text_from_anchor(document, line.layout.text_anchor),
                    page=page.page_number,
                    bbox=normalize_vertices(line.layout.bounding_poly.normalized_vertices),
                    confidence=getattr(line.layout, "confidence", None),
                )
            )
        for table in page.tables:
            elements.append(
                LayoutElement(
                    element_type="table",
                    text=" ".join(
                        filter(
                            None,
                            [
                                get_text_from_anchor(document, cell.layout.text_anchor)
                                for row in list(table.header_rows) + list(table.body_rows)
                                for cell in row.cells
                            ],
                        )
                    ),
                    page=page.page_number,
                    bbox=normalize_vertices(table.layout.bounding_poly.normalized_vertices),
                    confidence=getattr(table.layout, "confidence", None),
                )
            )
    return elements
