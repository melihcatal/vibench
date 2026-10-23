import os
from document_client import DocumentAIClient
from document_models import (
    DocumentResponse,
    DocumentPage,
    DocumentPageBlock,
    TextAnchor,
    TextSpan,
    BoundingPoly,
)
from google.cloud import documentai_v1 as documentai


def _get_text(
    document: documentai.Document, text_anchor: documentai.Document.TextAnchor
) -> str:
    """Helper to extract text from a text anchor."""
    if not text_anchor.text_segments:
        return ""

    full_text = ""
    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        full_text += document.text[start_index:end_index]
    return full_text


def extract_document_layout(
    file_content: bytes, mime_type: str, processor_id: str
) -> DocumentResponse:
    """
    Extracts blocks, lines, tables, or layout elements from a document using Google Document AI.
    """
    client = DocumentAIClient()
    document = client.process_document(file_content, mime_type, processor_id)

    pages_data = []
    for page in document.pages:
        blocks_data = []
        for block in page.blocks:
            bounding_poly_data = BoundingPoly(
                vertices=[
                    {"x": v.x, "y": v.y} for v in block.layout.bounding_poly.vertices
                ]
            )
            text_anchor_data = TextAnchor(
                text_segments=[
                    TextSpan(
                        offset=int(ts.start_index),
                        length=int(ts.end_index) - int(ts.start_index),
                    )
                    for ts in block.layout.text_anchor.text_segments
                ]
            )
            blocks_data.append(
                DocumentPageBlock(
                    bounding_poly=bounding_poly_data,
                    text_anchor=text_anchor_data,
                    type="block",  # Generic type for now
                )
            )

        for paragraph in page.paragraphs:
            bounding_poly_data = BoundingPoly(
                vertices=[
                    {"x": v.x, "y": v.y}
                    for v in paragraph.layout.bounding_poly.vertices
                ]
            )
            text_anchor_data = TextAnchor(
                text_segments=[
                    TextSpan(
                        offset=int(ts.start_index),
                        length=int(ts.end_index) - int(ts.start_index),
                    )
                    for ts in paragraph.layout.text_anchor.text_segments
                ]
            )
            blocks_data.append(
                DocumentPageBlock(
                    bounding_poly=bounding_poly_data,
                    text_anchor=text_anchor_data,
                    type="paragraph",
                )
            )

        for line in page.lines:
            bounding_poly_data = BoundingPoly(
                vertices=[
                    {"x": v.x, "y": v.y} for v in line.layout.bounding_poly.vertices
                ]
            )
            text_anchor_data = TextAnchor(
                text_segments=[
                    TextSpan(
                        offset=int(ts.start_index),
                        length=int(ts.end_index) - int(ts.start_index),
                    )
                    for ts in line.layout.text_anchor.text_segments
                ]
            )
            blocks_data.append(
                DocumentPageBlock(
                    bounding_poly=bounding_poly_data,
                    text_anchor=text_anchor_data,
                    type="line",
                )
            )

        for token in page.tokens:
            bounding_poly_data = BoundingPoly(
                vertices=[
                    {"x": v.x, "y": v.y} for v in token.layout.bounding_poly.vertices
                ]
            )
            text_anchor_data = TextAnchor(
                text_segments=[
                    TextSpan(
                        offset=int(ts.start_index),
                        length=int(ts.end_index) - int(ts.start_index),
                    )
                    for ts in token.layout.text_anchor.text_segments
                ]
            )
            blocks_data.append(
                DocumentPageBlock(
                    bounding_poly=bounding_poly_data,
                    text_anchor=text_anchor_data,
                    type="token",
                )
            )

        pages_data.append(
            DocumentPage(
                page_number=page.page_number,
                image_width=page.dimension.width,
                image_height=page.dimension.height,
                text=_get_text(document, page.layout.text_anchor),
                blocks=blocks_data,
                tables=[],
                form_fields=[],
            )
        )

    return DocumentResponse(text=document.text, pages=pages_data, entities=[])
