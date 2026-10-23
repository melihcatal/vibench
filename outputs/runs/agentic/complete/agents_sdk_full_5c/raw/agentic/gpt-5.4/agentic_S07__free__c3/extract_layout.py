from __future__ import annotations

from typing import List

from document_client import build_processor_name, get_documentai_client, get_processor_id, guess_mime_type
from document_models import DocumentRequest, LayoutElement, load_bytes, polygon_to_bbox
from google.cloud import documentai_v1 as documentai


LAYOUT_TYPES = {
    "paragraphs": "paragraph",
    "blocks": "block",
    "lines": "line",
    "tokens": "token",
    "tables": "table",
}


def _layout_text(document: documentai.Document, layout: documentai.Document.Page.Layout) -> str:
    parts = []
    for segment in layout.text_anchor.text_segments:
        parts.append(document.text[int(segment.start_index):int(segment.end_index)])
    return "".join(parts).strip()


def extract_layout(request: DocumentRequest) -> List[LayoutElement]:
    client = get_documentai_client()
    processor_name = build_processor_name(get_processor_id("DOCUMENTAI_LAYOUT_PROCESSOR_ID"))
    raw_document = documentai.RawDocument(
        content=load_bytes(request.file_path),
        mime_type=guess_mime_type(request.file_path, request.mime_type),
    )
    result = client.process_document(
        request=documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    )
    document = result.document
    elements: List[LayoutElement] = []
    for page in document.pages:
        for attr_name, kind in LAYOUT_TYPES.items():
            for item in getattr(page, attr_name, []):
                layout = item.layout if hasattr(item, "layout") else item
                elements.append(
                    LayoutElement(
                        kind=kind,
                        text=_layout_text(document, layout),
                        page=page.page_number,
                        bbox=polygon_to_bbox(layout.bounding_poly.normalized_vertices),
                        confidence=getattr(layout, "confidence", None),
                        metadata={"processor": processor_name},
                    )
                )
    return elements
