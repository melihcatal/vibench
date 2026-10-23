from __future__ import annotations

from typing import List

from document_client import document_to_dict, process_document, text_from_layout
from document_models import DocumentRequest, TableCell, TableResult


def extract_tables(request: DocumentRequest) -> TableResult:
    document = process_document(request, "GOOGLE_DOCUMENTAI_FORM_PARSER_PROCESSOR_ID")
    cells: List[TableCell] = []
    rows: List[List[str]] = []
    for page in document.pages:
        for table in page.tables:
            row_cursor = len(rows)
            all_rows = list(table.header_rows) + list(table.body_rows)
            for local_row_index, row in enumerate(all_rows):
                row_values: List[str] = []
                for col_index, cell in enumerate(row.cells):
                    text = text_from_layout(document, cell.layout)
                    row_values.append(text)
                    cells.append(
                        TableCell(
                            row_index=row_cursor + local_row_index,
                            column_index=col_index,
                            text=text,
                            row_span=int(cell.row_span or 1),
                            column_span=int(cell.col_span or 1),
                            confidence=float(cell.layout.confidence or 0.0),
                        )
                    )
                rows.append(row_values)
    return TableResult(
        cells=cells, rows=rows, provider_payload=document_to_dict(document)
    )
