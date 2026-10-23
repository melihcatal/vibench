import os
from typing import List, Dict, Any
import base64
import json
from google.cloud import documentai
from document_client import get_documentai_client
from document_models import TableResponse, Table, TableCell, TableExtractionRequest


def extract_tables(request: TableExtractionRequest) -> TableResponse:
    """Extract table cells and row structure from a document using Google Cloud Document AI."""

    client = get_documentai_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.getenv("DOCUMENT_AI_PROCESSOR_ID", "your-processor-id")

    if request.image_path:
        with open(request.image_path, "rb") as image_file:
            content = image_file.read()
    elif request.image_base64:
        content = base64.b64decode(request.image_base64)
    else:
        raise ValueError("Either image_path or image_base64 must be provided")

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    raw_document = documentai.RawDocument(
        content=content, mime_type=request.mime_type or "image/jpeg"
    )

    request_docai = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request_docai)
    document = result.document

    tables: List[Table] = []

    if hasattr(document, "pages"):
        for page in document.pages:
            for table_num, table in enumerate(page.tables):
                rows: List[List[TableCell]] = []

                for row in table.header_rows:
                    row_cells: List[TableCell] = []
                    for cell in row.cells:
                        cell_text = ""
                        if cell.layout and cell.layout.text_anchor:
                            cell_text = extract_text_from_anchor(
                                document.text, cell.layout.text_anchor
                            )
                        row_cells.append(
                            TableCell(
                                text=cell_text,
                                row_span=cell.row_span,
                                col_span=cell.col_span,
                            )
                        )
                    rows.append(row_cells)

                for row in table.body_rows:
                    row_cells: List[TableCell] = []
                    for cell in row.cells:
                        cell_text = ""
                        if cell.layout and cell.layout.text_anchor:
                            cell_text = extract_text_from_anchor(
                                document.text, cell.layout.text_anchor
                            )
                        row_cells.append(
                            TableCell(
                                text=cell_text,
                                row_span=cell.row_span,
                                col_span=cell.col_span,
                            )
                        )
                    rows.append(row_cells)

                tables.append(
                    Table(
                        rows=rows,
                        row_count=len(rows),
                        column_count=max(len(row) for row in rows) if rows else 0,
                    )
                )

    return TableResponse(
        tables=tables,
        provider="google_document_ai",
        model="form_parser",
        raw_response=result,
    )


def extract_text_from_anchor(full_text: str, text_anchor) -> str:
    """Extract text from a text anchor in Document AI response."""
    if not text_anchor.text_segments:
        return ""

    text_segment = text_anchor.text_segments[0]
    start_index = text_segment.start_index
    end_index = text_segment.end_index
    return full_text[start_index:end_index]
