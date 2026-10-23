from typing import List
from document_client import process_document
from document_models import Table, TableRow, TableCell, BoundingPoly, Point

def _get_text(element, text: str) -> str:
    text_anchor = element.layout.text_anchor
    if not text_anchor.text_segments:
        return ""
    start_index = int(text_anchor.text_segments[0].start_index)
    end_index = int(text_anchor.text_segments[0].end_index)
    return text[start_index:end_index]

def extract_document_tables(image_content: bytes) -> List[Table]:
    """
    Extracts tables from a document image using Google Cloud Document AI.

    Args:
        image_content: The byte content of the image file.

    Returns:
        A list of Table objects found in the document.
    """
    document = process_document(image_content)
    doc_text = document.text
    tables = []

    for page in document.pages:
        for table_idx, table_proto in enumerate(page.tables):
            
            def parse_rows(row_protos):
                rows = []
                for row in row_protos:
                    cells = []
                    for cell in row.cells:
                        cell_text = _get_text(cell, doc_text)
                        cell_poly = BoundingPoly(
                            vertices=[Point(x=v.x, y=v.y) for v in cell.layout.bounding_poly.vertices]
                        )
                        cells.append(TableCell(
                            text=cell_text,
                            bounding_poly=cell_poly,
                            confidence=cell.layout.confidence,
                            row_index=cell.row_index,
                            col_index=cell.col_index,
                            row_span=cell.row_span,
                            col_span=cell.col_span,
                        ))
                    rows.append(TableRow(cells=cells))
                return rows

            header_rows = parse_rows(table_proto.header_rows)
            body_rows = parse_rows(table_proto.body_rows)
            
            table_text = _get_text(table_proto, doc_text)
            table_poly = BoundingPoly(
                vertices=[Point(x=v.x, y=v.y) for v in table_proto.layout.bounding_poly.vertices]
            )

            tables.append(Table(
                text=table_text,
                bounding_poly=table_poly,
                confidence=table_proto.layout.confidence,
                header_rows=header_rows,
                body_rows=body_rows
            ))
            
    return tables
