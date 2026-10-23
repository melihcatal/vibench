from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import TableCell, TableResult, text_anchor_to_string


PROVIDER = "google-document-ai"


def _row_to_values(document, row) -> List[str]:
    return [text_anchor_to_string(document, cell.layout.text_anchor) for cell in row.cells]


def extract_tables(source: str, mime_type: str | None = None) -> List[TableResult]:
    document = process_document(source=source, mime_type=mime_type)
    results: List[TableResult] = []
    for page_index, page in enumerate(document.pages, start=1):
        for table in getattr(page, "tables", []):
            cells: List[TableCell] = []
            header_rows = [_row_to_values(document, row) for row in table.header_rows]
            body_rows = [_row_to_values(document, row) for row in table.body_rows]
            all_rows = list(table.header_rows) + list(table.body_rows)
            for r_index, row in enumerate(all_rows):
                for c_index, cell in enumerate(row.cells):
                    cells.append(
                        TableCell(
                            row_index=r_index,
                            column_index=c_index,
                            text=text_anchor_to_string(document, cell.layout.text_anchor),
                            row_span=getattr(cell, "row_span", 1),
                            col_span=getattr(cell, "col_span", 1),
                            confidence=getattr(cell.layout, "confidence", None),
                        )
                    )
            results.append(TableResult(page=page_index, header_rows=header_rows, body_rows=body_rows, cells=cells))
    return results
