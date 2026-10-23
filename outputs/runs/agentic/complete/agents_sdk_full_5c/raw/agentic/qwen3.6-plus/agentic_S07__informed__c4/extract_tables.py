"""
[SAME-SCENARIO] Extracts table cells and row structure from a document.

Provider: Google Document AI (google-cloud-documentai)
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model/Processor: Built-in Document OCR / Table parser processor
Service endpoint: documentai.googleapis.com
"""

from __future__ import annotations

import os
from typing import Optional, List

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import document as documentai_types

from document_client import load_image_bytes, get_google_project_id
from document_models import (
    TableStructure,
    TableCell,
    BoundingBox,
    OcrDocumentResult,
)


def extract_tables_from_document(
    file_path: str,
    project_id: Optional[str] = None,
    location: str = "us",
    processor_id: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> OcrDocumentResult:
    """
    Extract table cells and row/column structure from a document using
    Google Document AI (documentai.googleapis.com).

    Returns an OcrDocumentResult with populated tables containing
    TableCell and TableStructure objects.
    """
    project_id = project_id or get_google_project_id()
    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT environment variable or project_id argument is required"
        )

    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    client_options = ClientOptions(
        api_endpoint=f"{location}-documentai.googleapis.com"
    )

    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    raw_bytes = load_image_bytes(file_path)
    if mime_type is None:
        ext = os.path.splitext(file_path)[1].lower()
        mime_type = "application/pdf" if ext == ".pdf" else "image/png"

    raw_document = documentai.RawDocument(
        content=raw_bytes,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document
    full_text = document.text

    all_tables: List[TableStructure] = []
    page_count = len(document.pages)

    for page in document.pages:
        page_tables = _parse_page_tables(page, full_text)
        all_tables.extend(page_tables)

    return OcrDocumentResult(
        plain_text=full_text,
        tables=all_tables,
        page_count=page_count,
    )


def _parse_page_tables(
    page: documentai_types.Document.Page,
    full_text: str,
) -> List[TableStructure]:
    """Parse all tables from a single Document AI page."""
    tables: List[TableStructure] = []

    for docai_table in page.tables:
        table_structure = _parse_single_table(docai_table, full_text)
        tables.append(table_structure)

    return tables


def _parse_single_table(
    docai_table: documentai_types.Document.Page.Table,
    full_text: str,
) -> TableStructure:
    """Parse a single Document AI table into TableStructure."""
    cells: List[TableCell] = []
    header_row_count = len(getattr(docai_table, "header_rows", []))
    body_row_count = len(docai_table.body_rows)
    total_rows = header_row_count + body_row_count

    # Determine column count from body rows
    col_count = 0
    if docai_table.body_rows:
        col_count = max(
            (len(row.cells) for row in docai_table.body_rows),
            default=0,
        )
    if header_row_count > 0 and getattr(docai_table, "header_rows", []):
        header_cols = max(
            (len(row.cells) for row in docai_table.header_rows),
            default=0,
        )
        col_count = max(col_count, header_cols)

    row_offset = 0

    # Process header rows
    for header_row in getattr(docai_table, "header_rows", []):
        for cell in header_row.cells:
            cell_text = _extract_cell_text(cell, full_text)
            bbox = _bbox_from_cell(cell)
            cells.append(
                TableCell(
                    row_index=row_offset,
                    column_index=_cell_col_index(cell),
                    text=cell_text,
                    row_span=_cell_row_span(cell),
                    column_span=_cell_col_span(cell),
                    bounding_box=bbox,
                )
            )
        row_offset += 1

    # Process body rows
    for body_row in docai_table.body_rows:
        for cell in body_row.cells:
            cell_text = _extract_cell_text(cell, full_text)
            bbox = _bbox_from_cell(cell)
            cells.append(
                TableCell(
                    row_index=row_offset,
                    column_index=_cell_col_index(cell),
                    text=cell_text,
                    row_span=_cell_row_span(cell),
                    column_span=_cell_col_span(cell),
                    bounding_box=bbox,
                )
            )
        row_offset += 1

    bbox = _bbox_from_layout(docai_table.layout)

    return TableStructure(
        row_count=total_rows,
        column_count=col_count,
        cells=cells,
        bounding_box=bbox,
    )


def _extract_cell_text(
    cell: documentai_types.Document.Page.Table.DetectedCell,
    full_text: str,
) -> str:
    """Extract text from a table cell."""
    if cell.layout and cell.layout.text_anchor:
        start = int(cell.layout.text_anchor.text_segments[0].start_index)
        end = int(cell.layout.text_anchor.text_segments[-1].end_index)
        return full_text[start:end].strip()
    return ""


def _cell_col_index(
    cell: documentai_types.Document.Page.Table.DetectedCell,
) -> int:
    """Get column index from a cell."""
    return getattr(cell, "col_span", 0)


def _cell_row_span(
    cell: documentai_types.Document.Page.Table.DetectedCell,
) -> int:
    """Get row span from a cell."""
    return getattr(cell, "row_span", 1)


def _cell_col_span(
    cell: documentai_types.Document.Page.Table.DetectedCell,
) -> int:
    """Get column span from a cell."""
    return getattr(cell, "col_span", 1)


def _bbox_from_cell(
    cell: documentai_types.Document.Page.Table.DetectedCell,
) -> Optional[BoundingBox]:
    """Build BoundingBox from a table cell's layout."""
    return _bbox_from_layout(cell.layout)


def _bbox_from_layout(layout) -> Optional[BoundingBox]:
    """Build a BoundingBox from a layout element's bounding polygon."""
    if layout and layout.bounding_poly:
        vertices = layout.bounding_poly.normalized_vertices
        if vertices:
            return BoundingBox.from_docai_vertices(
                [{"x": v.x, "y": v.y} for v in vertices]
            )
    return None
