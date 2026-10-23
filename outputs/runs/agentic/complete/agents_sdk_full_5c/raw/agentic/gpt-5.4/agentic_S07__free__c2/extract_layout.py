from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import LayoutElement, get_text, normalize_polygon


def extract_layout(file_path: str) -> List[LayoutElement]:
    document = process_document(file_path)
    elements: List[LayoutElement] = []
    full_text = document.text or ""

    for page in document.pages:
        page_number = int(page.page_number)

        for block in page.blocks:
            text = get_text(block.layout.text_anchor, full_text)
            elements.append(
                LayoutElement(
                    kind="block",
                    text=text,
                    page=page_number,
                    bbox=normalize_polygon(block.layout.bounding_poly),
                    confidence=float(block.layout.confidence) if block.layout.confidence is not None else None,
                )
            )

        for line in page.lines:
            text = get_text(line.layout.text_anchor, full_text)
            elements.append(
                LayoutElement(
                    kind="line",
                    text=text,
                    page=page_number,
                    bbox=normalize_polygon(line.layout.bounding_poly),
                    confidence=float(line.layout.confidence) if line.layout.confidence is not None else None,
                )
            )

        for table in page.tables:
            header_count = len(table.header_rows)
            body_count = len(table.body_rows)
            elements.append(
                LayoutElement(
                    kind="table",
                    text=f"table headers={header_count} rows={body_count}",
                    page=page_number,
                    bbox=normalize_polygon(table.layout.bounding_poly),
                    confidence=float(table.layout.confidence) if table.layout.confidence is not None else None,
                    metadata={"header_rows": header_count, "body_rows": body_count},
                )
            )

    return elements
