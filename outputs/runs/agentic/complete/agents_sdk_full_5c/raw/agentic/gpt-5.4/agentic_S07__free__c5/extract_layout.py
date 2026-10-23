from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import LayoutElement, normalize_bbox, text_anchor_to_string


PROVIDER = "google-document-ai"


def extract_layout(source: str, mime_type: str | None = None) -> List[LayoutElement]:
    document = process_document(source=source, mime_type=mime_type)
    elements: List[LayoutElement] = []
    for page_index, page in enumerate(document.pages, start=1):
        for block in getattr(page, "blocks", []):
            elements.append(
                LayoutElement(
                    element_type="block",
                    text=text_anchor_to_string(document, block.layout.text_anchor),
                    page=page_index,
                    confidence=getattr(block.layout, "confidence", None),
                    bbox=normalize_bbox(getattr(block.layout.bounding_poly, "normalized_vertices", None) or getattr(block.layout.bounding_poly, "vertices", None)),
                    raw={"provider": PROVIDER},
                )
            )
        for line in getattr(page, "lines", []):
            elements.append(
                LayoutElement(
                    element_type="line",
                    text=text_anchor_to_string(document, line.layout.text_anchor),
                    page=page_index,
                    confidence=getattr(line.layout, "confidence", None),
                    bbox=normalize_bbox(getattr(line.layout.bounding_poly, "normalized_vertices", None) or getattr(line.layout.bounding_poly, "vertices", None)),
                    raw={"provider": PROVIDER},
                )
            )
        for table in getattr(page, "tables", []):
            table_text = []
            for row in list(table.header_rows) + list(table.body_rows):
                row_values = [text_anchor_to_string(document, cell.layout.text_anchor) for cell in row.cells]
                table_text.append(" | ".join(row_values))
            elements.append(
                LayoutElement(
                    element_type="table",
                    text="\n".join(table_text),
                    page=page_index,
                    confidence=None,
                    bbox=normalize_bbox(getattr(table.layout.bounding_poly, "normalized_vertices", None) or getattr(table.layout.bounding_poly, "vertices", None)),
                    raw={"provider": PROVIDER},
                )
            )
    return elements
