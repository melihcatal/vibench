from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import TableCell, TableResult, get_text


def _row_to_strings(row, full_text: str) -> List[str]:
    values: List[str] = []
    for cell in row.cells:
        values.append(get_text(cell.layout.text_anchor, full_text))
    return values


def extract_tables(file_path: str) -> List[TableResult]:
    document = process_document(file_path)
    full_text = document.text or ""
    tables: List[TableResult] = []

    for page in document.pages:
        page_number = int(page.page_number)
        for table in page.tables:
            result = TableResult(page=page_number)

            for row in table.header_rows:
                result.header_rows.append(_row_to_strings(row, full_text))

            for row_index, row in enumerate(table.body_rows):
                result.rows.append(_row_to_strings(row, full_text))
                for column_index, cell in enumerate(row.cells):
                    result.cells.append(
                        TableCell(
                            row_index=row_index,
                            column_index=column_index,
                            text=get_text(cell.layout.text_anchor, full_text),
                            row_span=int(cell.row_span or 1),
                            col_span=int(cell.col_span or 1),
                            confidence=float(cell.layout.confidence) if cell.layout.confidence is not None else None,
                        )
                    )

            tables.append(result)

    return tables
