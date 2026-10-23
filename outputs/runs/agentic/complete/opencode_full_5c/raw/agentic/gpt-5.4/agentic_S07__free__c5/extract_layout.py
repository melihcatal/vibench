from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import (
    DocumentInput,
    LayoutElement,
    get_text_anchor_text,
    normalize_bbox,
)


def extract_layout(document_input: DocumentInput) -> List[LayoutElement]:
    payload = {
        "skipHumanReview": True,
        "rawDocument": document_input.as_google_document()
        if document_input.bytes_base64
        else None,
        "gcsDocument": document_input.as_google_document()
        if document_input.source_uri
        else None,
        "processOptions": {
            "ocrConfig": {"premiumFeatures": {"enableSelectionMarkDetection": True}}
        },
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = process_document(payload)
    document = response.get("document", {})
    elements: List[LayoutElement] = []
    for page_index, page in enumerate(document.get("pages", []), start=1):
        for block in page.get("blocks", []):
            layout = block.get("layout", {})
            elements.append(
                LayoutElement(
                    page=page_index,
                    element_type="block",
                    text=get_text_anchor_text(document, layout.get("textAnchor")),
                    confidence=float(layout.get("confidence", 0.0)),
                    bbox=normalize_bbox(layout.get("boundingPoly", {}).get("vertices")),
                )
            )
        for line in page.get("lines", []):
            layout = line.get("layout", {})
            elements.append(
                LayoutElement(
                    page=page_index,
                    element_type="line",
                    text=get_text_anchor_text(document, layout.get("textAnchor")),
                    confidence=float(layout.get("confidence", 0.0)),
                    bbox=normalize_bbox(layout.get("boundingPoly", {}).get("vertices")),
                )
            )
        for table in page.get("tables", []):
            layout = table.get("layout", {})
            elements.append(
                LayoutElement(
                    page=page_index,
                    element_type="table",
                    text=get_text_anchor_text(document, layout.get("textAnchor")),
                    confidence=float(layout.get("confidence", 0.0)),
                    bbox=normalize_bbox(layout.get("boundingPoly", {}).get("vertices")),
                )
            )
    return elements
