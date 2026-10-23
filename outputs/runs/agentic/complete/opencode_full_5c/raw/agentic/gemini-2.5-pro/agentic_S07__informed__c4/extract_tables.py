from typing import List
from document_client import DocumentAIClient
from document_models import Table, Cell, BoundingBox


def _get_text(text_anchor, full_text):
    if not text_anchor.text_segments:
        return ""
    return "".join(
        full_text[int(segment.start_index) : int(segment.end_index)]
        for segment in text_anchor.text_segments
    )


def _get_bounding_box(bounding_poly) -> BoundingBox:
    if not bounding_poly or not bounding_poly.normalized_vertices:
        return BoundingBox(0, 0, 0, 0)

    vertices = bounding_poly.normalized_vertices
    return BoundingBox(
        x1=vertices[0].x, y1=vertices[0].y, x2=vertices[2].x, y2=vertices[2].y
    )


def extract_tables_from_document(file_path: str) -> List[Table]:
    """
    Extracts table cells and row structure from a document.
    """
    client = DocumentAIClient()
    document = client.process_document(file_path)

    tables = []
    for page in document.pages:
        for table_idx, page_table in enumerate(page.tables):
            cells = []

            # Header rows
            for row in page_table.header_rows:
                for cell in row.cells:
                    cells.append(
                        Cell(
                            text=_get_text(cell.layout.text_anchor, document.text),
                            row_index=cell.row_span,
                            column_index=cell.col_span,
                            row_span=cell.row_span,
                            column_span=cell.col_span,
                            bounding_box=_get_bounding_box(cell.layout.bounding_poly),
                        )
                    )

            # Body rows
            for row in page_table.body_rows:
                for cell in row.cells:
                    cells.append(
                        Cell(
                            text=_get_text(cell.layout.text_anchor, document.text),
                            row_index=cell.row_span,
                            column_index=cell.col_span,
                            row_span=cell.row_span,
                            column_span=cell.col_span,
                            bounding_box=_get_bounding_box(cell.layout.bounding_poly),
                        )
                    )

            tables.append(
                Table(
                    rows=len(page_table.header_rows) + len(page_table.body_rows),
                    columns=max(
                        len(r.cells)
                        for r in page_table.header_rows + page_table.body_rows
                    )
                    if page_table.header_rows or page_table.body_rows
                    else 0,
                    cells=cells,
                    bounding_box=_get_bounding_box(page_table.layout.bounding_poly),
                )
            )

    return tables
