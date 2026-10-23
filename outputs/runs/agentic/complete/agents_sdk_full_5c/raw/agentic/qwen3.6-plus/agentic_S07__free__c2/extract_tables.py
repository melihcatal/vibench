"""
[SAME-SCENARIO] Extract table cells and row structure from a document.
Uses Google Cloud Document AI for table detection and structured extraction,
identifying table boundaries, rows, columns, and cell content.
"""

import os
from typing import Optional, List, Dict, Any
from google.cloud import documentai_v1
from google.cloud.documentai_v1 import DocumentProcessorServiceClient

from document_client import (
    GOOGLE_CLOUD_PROJECT,
    GOOGLE_CLOUD_LOCATION,
)
from document_models import (
    TableResponse,
    ExtractedTable,
    TableRow,
    TableCell,
    BoundingBox,
    normalize_vision_vertices,
)


GOOGLE_CLOUD_DOCUMENT_AI_TABLE_MODEL = "document-ai-table-extraction"
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")


class DocumentAIClient:
    """Client wrapper for Google Cloud Document AI table extraction."""

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
    ):
        self.project = project or GOOGLE_CLOUD_PROJECT
        self.location = location or GOOGLE_CLOUD_LOCATION
        self.client = DocumentProcessorServiceClient()

    def get_processor_name(self, processor_id: str) -> str:
        """Build the full processor resource name for Document AI."""
        return self.client.processor_path(
            project=self.project,
            location=self.location,
            processor=processor_id,
        )

    def process_document(
        self,
        file_path: str,
        processor_id: str,
        mime_type: str = "application/pdf",
    ) -> documentai_v1.Document:
        """Process a document using a Document AI processor for table extraction."""
        processor_name = self.get_processor_name(processor_id)

        with open(file_path, "rb") as f:
            file_content = f.read()

        raw_document = documentai_v1.RawDocument(
            content=file_content,
            mime_type=mime_type,
        )

        request = documentai_v1.ProcessRequest(
            name=processor_name,
            raw_document=raw_document,
        )

        result = self.client.process_document(request=request)
        return result.document


def extract_tables_from_document(
    file_path: str,
    processor_id: str,
    mime_type: str = "application/pdf",
) -> TableResponse:
    """
    Extract tables from a document using Google Cloud Document AI.

    Uses the documentai.googleapis.com endpoint with table extraction
    capabilities to detect table structures, rows, and cells.

    Args:
        file_path: Path to the document file (PDF or image).
        processor_id: Document AI processor ID configured for table extraction.
        mime_type: MIME type of the input document.

    Returns:
        TableResponse containing all detected tables with row and cell structure.
    """
    doc_ai_client = DocumentAIClient()
    document = doc_ai_client.process_document(file_path, processor_id, mime_type)

    tables = []
    for page in document.pages:
        page_width = float(getattr(page, 'dimension', None).width if hasattr(page, 'dimension') else 1.0) or 1.0
        page_height = float(getattr(page, 'dimension', None).height if hasattr(page, 'dimension') else 1.0) or 1.0

        for table in page.tables:
            extracted_table = _parse_document_ai_table(
                document, table, page_width, page_height
            )
            tables.append(extracted_table)

    return TableResponse(
        tables=tables,
        page_count=len(document.pages),
    )


def _parse_document_ai_table(
    document: documentai_v1.Document,
    table,
    page_width: float,
    page_height: float,
) -> ExtractedTable:
    """Parse a single Document AI table into our ExtractedTable model."""
    rows = []
    table_id = f"table_{id(table)}"

    bounding_box = None
    if table.layout and table.layout.bounding_poly:
        bounding_box = _extract_bounding_box(table.layout.bounding_poly, page_width, page_height)

    header_rows = _get_header_row_indices(table)

    for i, row in enumerate(table.body_rows):
        cells = []
        for j, cell in enumerate(row.cells):
            cell_text = _extract_cell_text(document, cell)
            confidence = getattr(cell, 'confidence', 0.0) or 0.0

            cell_bbox = None
            if cell.layout and cell.layout.bounding_poly:
                cell_bbox = _extract_bounding_box(cell.layout.bounding_poly, page_width, page_height)

            is_header = i in header_rows

            cells.append(
                TableCell(
                    row_index=i,
                    col_index=j,
                    text=cell_text.strip(),
                    confidence=confidence,
                    bounding_box=cell_bbox,
                    is_header=is_header,
                )
            )

        rows.append(TableRow(cells=cells, row_index=i))

    return ExtractedTable(
        rows=rows,
        bounding_box=bounding_box,
        table_id=table_id,
    )


def _extract_cell_text(document: documentai_v1.Document, cell) -> str:
    """Extract text from a table cell using Document AI text anchor."""
    if not cell.layout or not cell.layout.text_anchor:
        return ""

    text_segments = cell.layout.text_anchor.text_segments
    full_text = document.text
    result_parts = []

    for segment in text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        result_parts.append(full_text[start_index:end_index])

    return "".join(result_parts)


def _get_header_row_indices(table) -> set:
    """Identify header row indices from Document AI table header_rows."""
    header_rows = set()
    if hasattr(table, 'header_rows') and table.header_rows:
        for hr in table.header_rows:
            if hasattr(hr, 'row_index'):
                header_rows.add(int(hr.row_index))
    return header_rows


def _extract_bounding_box(bounding_poly, page_width: float, page_height: float) -> BoundingBox:
    """Convert Document AI bounding poly to normalized BoundingBox."""
    vertices = bounding_poly.vertices if hasattr(bounding_poly, 'vertices') else []
    x_coords = []
    y_coords = []

    for vertex in vertices:
        if hasattr(vertex, 'x'):
            x_coords.append(float(vertex.x) / page_width if page_width > 0 else 0)
        if hasattr(vertex, 'y'):
            y_coords.append(float(vertex.y) / page_height if page_height > 0 else 0)

    if not x_coords or not y_coords:
        return BoundingBox(0.0, 0.0, 1.0, 1.0)

    return BoundingBox(
        x_min=min(x_coords),
        y_min=min(y_coords),
        x_max=max(x_coords),
        y_max=max(y_coords),
    )


def extract_tables_from_vision_api(
    image_path: str,
    language_hints: Optional[List[str]] = None,
) -> TableResponse:
    """
    Fallback table extraction using Google Cloud Vision API DOCUMENT_TEXT_DETECTION.
    Less precise than Document AI but useful when no processor is available.
    """
    from google.cloud import vision_v1
    from document_client import GoogleVisionClient, get_vision_client
    from document_models import build_vision_image_context

    client = get_vision_client()
    image_content = client.encode_image_to_base64(image_path)

    image_context = None
    if language_hints:
        image_context = build_vision_image_context(language_hints=language_hints)

    features = [client.create_feature("DOCUMENT_TEXT_DETECTION")]
    response = client.annotate_image(
        image_content=image_content,
        features=features,
        image_context=image_context,
    )

    tables = _parse_vision_tables(response, image_path)

    return TableResponse(
        tables=tables,
        page_count=1,
    )


def _parse_vision_tables(response, image_path: str) -> List[ExtractedTable]:
    """Heuristically parse tables from Google Vision API response."""
    from PIL import Image
    import io

    tables = []
    full_text = response.full_text_annotation

    if not full_text:
        return tables

    text = full_text.text.strip()
    lines = text.split("\n")

    table_lines = []
    in_table = False
    table_start = 0

    for i, line in enumerate(lines):
        cols = line.split("\t") if "\t" in line else None
        if cols and len(cols) >= 2:
            if not in_table:
                in_table = True
                table_start = i
            table_lines.append(line)
        else:
            if in_table:
                table = _build_table_from_lines(table_lines, table_start)
                tables.append(table)
                table_lines = []
                in_table = False

    if in_table and table_lines:
        table = _build_table_from_lines(table_lines, table_start)
        tables.append(table)

    return tables


def _build_table_from_lines(lines: List[str], start_row: int) -> ExtractedTable:
    """Build an ExtractedTable from tab-separated lines."""
    rows = []
    for i, line in enumerate(lines):
        cols = line.split("\t")
        cells = []
        for j, col_text in enumerate(cols):
            cells.append(
                TableCell(
                    row_index=i,
                    col_index=j,
                    text=col_text.strip(),
                    confidence=0.5,
                    is_header=(i == 0),
                )
            )
        rows.append(TableRow(cells=cells, row_index=i))

    return ExtractedTable(rows=rows, table_id=f"vision_table_{start_row}")


if __name__ == "__main__":
    doc_path = os.environ.get("DOCUMENT_PATH", "sample_document.pdf")
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "table-processor")
    result = extract_tables_from_document(doc_path, processor_id)
    for table in result.tables:
        print(f"Table {table.table_id}: {len(table.rows)} rows")
        for row in table.rows:
            print("  ", [cell.text for cell in row.cells])
