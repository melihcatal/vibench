import os
from document_client import DocumentAIClient
from document_models import (
    DocumentResponse,
    DocumentPage,
    DocumentPageTableProperty,
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


def extract_document_tables(
    file_content: bytes, mime_type: str, processor_id: str
) -> DocumentResponse:
    """
    Extracts table cells and row structure from a document using Google Document AI.
    """
    client = DocumentAIClient()
    document = client.process_document(file_content, mime_type, processor_id)

    pages_data = []
    for page in document.pages:
        tables_data = []
        for table in page.tables:
            cells_data = []
            for cell in table.body_rows:
                for table_cell in cell.cells:
                    cells_data.append(
                        {
                            "row_index": table_cell.row_span.start,
                            "col_index": table_cell.col_span.start,
                            "text": _get_text(document, table_cell.layout.text_anchor),
                        }
                    )

            bounding_poly_data = BoundingPoly(
                vertices=[
                    {"x": v.x, "y": v.y} for v in table.layout.bounding_poly.vertices
                ]
            )
            text_anchor_data = TextAnchor(
                text_segments=[
                    TextSpan(
                        offset=int(ts.start_index),
                        length=int(ts.end_index) - int(ts.start_index),
                    )
                    for ts in table.layout.text_anchor.text_segments
                ]
            )

            tables_data.append(
                DocumentPageTableProperty(
                    text_anchor=text_anchor_data,
                    bounding_poly=bounding_poly_data,
                    num_rows=table.header_rows[0].cells[0].row_span.end
                    if table.header_rows
                    else len(table.body_rows),  # Simplified
                    num_columns=table.header_rows[0].cells[0].col_span.end
                    if table.header_rows
                    else max(c["col_index"] for c in cells_data) + 1
                    if cells_data
                    else 0,  # Simplified
                    cells=cells_data,
                )
            )

        pages_data.append(
            DocumentPage(
                page_number=page.page_number,
                image_width=page.dimension.width,
                image_height=page.dimension.height,
                text=_get_text(document, page.layout.text_anchor),
                blocks=[],
                tables=tables_data,
                form_fields=[],
            )
        )

    return DocumentResponse(text=document.text, pages=pages_data, entities=[])
