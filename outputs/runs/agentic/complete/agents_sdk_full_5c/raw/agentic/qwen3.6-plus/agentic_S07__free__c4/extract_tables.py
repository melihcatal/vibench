"""
extract_tables.py - Extracts table cells and row structure from a document
using Google Cloud Document AI API.

Provider: Google Cloud Document AI
Model: document_preprocess (layout parsing with table detection)
"""

from typing import Optional, Dict, Any, Union

from google.cloud import documentai_v1 as documentai
from google.api_core.exceptions import GoogleAPICallError

from document_client import (
    DocumentClientConfig,
    get_google_documentai_client,
    normalize_image_to_bytes,
)
from document_models import (
    TableResult,
    ExtractedTable,
    TableCell,
    BoundingBox,
    normalize_google_table_to_cells,
)


def extract_tables_from_document(
    document_data: Union[str, bytes, Any],
    mime_type: str = "image/png",
    client: Optional[Any] = None,
    processor_name: Optional[str] = None,
) -> TableResult:
    """
    Extract tables with cell-level detail from a document using
    Google Cloud Document AI.

    Args:
        document_data: Document as bytes, file path string, or file-like object.
        mime_type: MIME type of the document (e.g., "image/png", "application/pdf").
        client: Optional tuple of (DocumentProcessorServiceClient, processor_name).
        processor_name: Optional explicit processor resource name.

    Returns:
        TableResult containing extracted tables with cell structure.
    """
    if client is None:
        client, processor_name = get_google_documentai_client()
    else:
        client, processor_name = client

    doc_bytes = normalize_image_to_bytes(document_data)

    raw_document = documentai.RawDocument(
        content=doc_bytes,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    try:
        result = client.process_document(request=request)
    except GoogleAPICallError as e:
        raise RuntimeError(f"Google Document AI table extraction failed: {e}") from e

    document = result.document
    return _parse_google_document_tables(document)


def _parse_google_document_tables(
    document: documentai.Document,
) -> TableResult:
    """Parse Google Document AI response into normalized TableResult."""
    tables = []

    for table in document.tables:
        header_rows = []
        body_rows = []

        # Parse header rows
        for header_row in table.header_rows:
            cells = []
            for cell in header_row.cells:
                cell_content = _extract_text_from_element(cell.layout.text_anchor, document)
                bbox = _bbox_from_layout(cell.layout)
                cells.append({
                    "content": cell_content,
                    "bounding_box": bbox,
                    "confidence": cell.confidence if hasattr(cell, "confidence") else 0.0,
                })
            header_rows.append({"cells": cells})

        # Parse body rows
        for body_row in table.body_rows:
            cells = []
            for cell in body_row.cells:
                cell_content = _extract_text_from_element(cell.layout.text_anchor, document)
                bbox = _bbox_from_layout(cell.layout)
                cells.append({
                    "content": cell_content,
                    "bounding_box": bbox,
                    "confidence": cell.confidence if hasattr(cell, "confidence") else 0.0,
                })
            body_rows.append({"cells": cells})

        table_data = {
            "header_rows": header_rows,
            "body_rows": body_rows,
        }

        table_cells = normalize_google_table_to_cells(table_data, header_rows=len(header_rows))

        bbox = _bbox_from_layout(table.layout) if hasattr(table, "layout") else None

        extracted_table = ExtractedTable(
            row_count=len(header_rows) + len(body_rows),
            column_count=_compute_max_columns(header_rows, body_rows),
            cells=table_cells,
            bounding_box=bbox,
            caption=None,
        )
        tables.append(extracted_table)

    page_dimensions = None
    if document.pages:
        page = document.pages[0]
        if hasattr(page, "dimension"):
            page_dimensions = {
                "width": page.dimension.width,
                "height": page.dimension.height,
                "unit": page.dimension.unit,
            }

    return TableResult(
        tables=tables,
        page_dimensions=page_dimensions,
    )


def _extract_text_from_element(
    text_anchor,
    document: documentai.Document,
) -> str:
    """Extract text content from a Document AI TextAnchor element."""
    if not text_anchor or not hasattr(text_anchor, "text_segments"):
        return ""

    text_content = ""
    for segment in text_anchor.text_segments:
        start = segment.start_index
        end = segment.end_index
        if hasattr(document, "text") and document.text:
            text_content += document.text[start:end]
    return text_content.strip()


def _bbox_from_layout(layout) -> Optional[Dict[str, float]]:
    """Extract bounding box from a Document AI layout element."""
    if not hasattr(layout, "bounding_poly") or layout.bounding_poly is None:
        return None

    poly = layout.bounding_poly
    if not hasattr(poly, "vertices") or not poly.vertices:
        return None

    polygon = []
    for vertex in poly.vertices:
        polygon.append(vertex.x)
        polygon.append(vertex.y)

    if len(polygon) >= 8:
        return BoundingBox.from_polygon(polygon).to_dict()
    return None


def _compute_max_columns(header_rows: list, body_rows: list) -> int:
    """Compute the maximum number of columns across all rows."""
    all_rows = header_rows + body_rows
    if not all_rows:
        return 0
    return max(len(row.get("cells", [])) for row in all_rows)


def extract_tables_from_gcs_uri(
    gcs_uri: str,
    mime_type: str = "application/pdf",
    client: Optional[Any] = None,
    processor_name: Optional[str] = None,
) -> TableResult:
    """
    Extract tables from a document stored in Google Cloud Storage.

    Args:
        gcs_uri: GCS URI (e.g., "gs://bucket/document.pdf").
        mime_type: MIME type of the document.
        client: Optional tuple of (client, processor_name).
        processor_name: Optional explicit processor resource name.

    Returns:
        TableResult with extracted table data.
    """
    if client is None:
        client, processor_name = get_google_documentai_client()
    else:
        client, processor_name = client

    gcs_document = documentai.GcsDocument(
        gcs_uri=gcs_uri,
        mime_type=mime_type,
    )

    gcs_documents = documentai.GcsDocuments(
        documents=[gcs_document],
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        gcs_documents=gcs_documents,
    )

    try:
        result = client.process_document(request=request)
    except GoogleAPICallError as e:
        raise RuntimeError(f"Google Document AI GCS table extraction failed: {e}") from e

    document = result.document
    return _parse_google_document_tables(document)
