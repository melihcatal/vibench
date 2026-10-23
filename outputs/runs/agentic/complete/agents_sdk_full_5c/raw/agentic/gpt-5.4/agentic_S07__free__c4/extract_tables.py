from __future__ import annotations

from typing import List

from document_client import process_document_bytes
from document_models import TableCell, TableResult, get_text_from_anchor


DEFAULT_MIME_TYPE = "image/png"


def _convert_row(document, row, row_index: int) -> List[TableCell]:
    cells: List[TableCell] = []
    for column_index, cell in enumerate(row.cells):
        cells.append(
            TableCell(
                row_index=row_index,
                column_index=column_index,
                text=get_text_from_anchor(document, cell.layout.text_anchor),
                row_span=int(getattr(cell, "row_span", 1) or 1),
                col_span=int(getattr(cell, "col_span", 1) or 1),
                confidence=getattr(cell.layout, "confidence", None),
            )
        )
    return cells


def extract_tables(file_path: str, mime_type: str = DEFAULT_MIME_TYPE) -> List[TableResult]:
    with open(file_path, "rb") as f:
        result = process_document_bytes(f.read(), mime_type)
    document = result.document
    extracted: List[TableResult] = []
    for page in document.pages:
        for table in page.tables:
            extracted.append(
                TableResult(
                    page=page.page_number,
                    header_rows=[
                        _convert_row(document, row, idx) for idx, row in enumerate(table.header_rows)
                    ],
                    body_rows=[
                        _convert_row(document, row, idx) for idx, row in enumerate(table.body_rows)
                    ],
                )
            )
    return extracted
