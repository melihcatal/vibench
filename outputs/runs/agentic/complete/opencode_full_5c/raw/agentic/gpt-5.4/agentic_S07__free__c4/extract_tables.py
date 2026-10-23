from __future__ import annotations

from typing import List

from document_client import (
    build_process_request,
    document_to_dict,
    get_documentai_client,
    get_processor_name,
)
from document_models import DocumentInput, TableCell, TableExtractionResult, TableResult


def extract_tables(
    document: DocumentInput, processor_id: str | None = None
) -> TableExtractionResult:
    client = get_documentai_client()
    request = build_process_request(
        document, get_processor_name(processor_id=processor_id)
    )
    response = client.process_document(request=request)
    processed = response.document
    tables: List[TableResult] = []
    for page_index, page in enumerate(processed.pages, start=1):
        for table in page.tables:
            cells: List[TableCell] = []
            row_index = 0
            max_col = 0
            for row in list(table.header_rows) + list(table.body_rows):
                col_index = 0
                for cell in row.cells:
                    cells.append(
                        TableCell(
                            row_index=row_index,
                            column_index=col_index,
                            text=_anchor_text(processed.text, cell.layout.text_anchor),
                            row_span=int(getattr(cell, "row_span", 1) or 1),
                            column_span=int(getattr(cell, "col_span", 1) or 1),
                            confidence=getattr(cell.layout, "confidence", None),
                        )
                    )
                    col_index += int(getattr(cell, "col_span", 1) or 1)
                max_col = max(max_col, col_index)
                row_index += 1
            tables.append(
                TableResult(
                    page=page_index,
                    row_count=row_index,
                    column_count=max_col,
                    cells=cells,
                )
            )
    return TableExtractionResult(
        provider="google_document_ai",
        tables=tables,
        raw_response=document_to_dict(processed),
    )


def _anchor_text(full_text: str, anchor) -> str:
    if not getattr(anchor, "text_segments", None):
        return ""
    return "".join(
        full_text[int(getattr(seg, "start_index", 0) or 0) : int(seg.end_index)]
        for seg in anchor.text_segments
    ).strip()
