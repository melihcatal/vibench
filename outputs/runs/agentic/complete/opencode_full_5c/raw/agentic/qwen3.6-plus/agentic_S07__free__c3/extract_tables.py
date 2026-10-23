from document_client import get_google_document_ai_client
from document_models import (
    TableResponse,
    Table,
    TableRow,
    TableCell,
    BoundingBox,
    normalize_bounding_box,
    normalize_confidence,
)

GOOGLE_DOC_AI_PROCESSOR_TYPE = "document-tables-parser"
GOOGLE_DOC_AI_MODEL_ID = "builtin/latest"


def extract_tables_from_document(
    document_bytes: bytes,
    mime_type: str = "application/pdf",
) -> TableResponse:
    client, project_id, location = get_google_document_ai_client()

    processor_display_name = "table-extraction-processor"
    processors = client.list_processors(
        parent=f"projects/{project_id}/locations/{location}"
    )
    processor_name = None
    for proc in processors:
        if proc.display_name == processor_display_name:
            processor_name = proc.name
            break

    if processor_name is None:
        raise ValueError(
            f"Processor '{processor_display_name}' not found. "
            f"Create a {GOOGLE_DOC_AI_PROCESSOR_TYPE} processor in Google Cloud Document AI."
        )

    from google.cloud.documentai_v1.types import document as doc_types
    from google.cloud.documentai_v1 import ProcessRequest

    raw_document = doc_types.RawDocument(
        content=document_bytes,
        mime_type=mime_type,
    )

    request = ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document

    tables = []

    for page in document.pages:
        for table in page.tables:
            table_rows = []
            max_row = 0
            max_col = 0

            for row_idx, row in enumerate(table.header_rows):
                cells = []
                for cell in row.cells:
                    cell_text = _extract_cell_text(document, cell)
                    bbox = _parse_google_bounding_box(cell.layout.bounding_poly)
                    tc = TableCell(
                        text=cell_text,
                        row_index=row_idx,
                        col_index=cell.col_span if hasattr(cell, "col_span") else 0,
                        row_span=1,
                        col_span=cell.col_span if hasattr(cell, "col_span") else 1,
                        confidence=normalize_confidence(cell.confidence),
                        bounding_box=bbox,
                    )
                    cells.append(tc)
                    if hasattr(cell, "col_span"):
                        max_col = max(max_col, cell.col_span)
                table_rows.append(TableRow(cells=cells, row_index=row_idx))

            for row_idx_offset, row in enumerate(table.body_rows):
                row_idx = len(table.header_rows) + row_idx_offset
                cells = []
                for cell in row.cells:
                    cell_text = _extract_cell_text(document, cell)
                    bbox = _parse_google_bounding_box(cell.layout.bounding_poly)
                    tc = TableCell(
                        text=cell_text,
                        row_index=row_idx,
                        col_index=cell.col_span if hasattr(cell, "col_span") else 0,
                        row_span=1,
                        col_span=cell.col_span if hasattr(cell, "col_span") else 1,
                        confidence=normalize_confidence(cell.confidence),
                        bounding_box=bbox,
                    )
                    cells.append(tc)
                    if hasattr(cell, "col_span"):
                        max_col = max(max_col, cell.col_span)
                table_rows.append(TableRow(cells=cells, row_index=row_idx))

            table_bbox = _parse_google_bounding_box(table.layout.bounding_poly)
            table_obj = Table(
                rows=table_rows,
                confidence=normalize_confidence(table.confidence),
                bounding_box=table_bbox,
            )
            tables.append(table_obj)

    page_width = 1.0
    page_height = 1.0
    if document.pages:
        dim = document.pages[0].dimension
        page_width = dim.width
        page_height = dim.height

    return TableResponse(
        tables=tables,
        page_width=page_width,
        page_height=page_height,
    )


def _extract_cell_text(document, cell) -> str:
    text = ""
    if (
        cell.layout
        and cell.layout.text_anchor
        and cell.layout.text_anchor.text_segments
    ):
        for segment in cell.layout.text_anchor.text_segments:
            text += document.text[segment.start_index : segment.end_index]
    return text.strip()


def _parse_google_bounding_box(bounding_poly) -> BoundingBox:
    if not bounding_poly or not bounding_poly.vertices:
        return BoundingBox(x=0.0, y=0.0, width=0.0, height=0.0)
    points = [(v.x, v.y) for v in bounding_poly.vertices]
    return normalize_bounding_box(points)
