from __future__ import annotations

from document_client import get_document_intelligence_client
from document_models import (
    DocumentSource,
    TableCell,
    TableExtractionResult,
    TableResult,
    load_binary,
    normalize_text,
)


def extract_tables(source: DocumentSource) -> TableExtractionResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=load_binary(source),
    )
    result = poller.result()
    tables = []
    for table in result.tables or []:
        cells = []
        for cell in table.cells or []:
            cells.append(
                TableCell(
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    text=normalize_text(cell.content),
                    row_span=cell.row_span or 1,
                    column_span=cell.column_span or 1,
                    confidence=getattr(cell, "confidence", None),
                )
            )
        page = (
            (table.bounding_regions or [None])[0].page_number
            if table.bounding_regions
            else 1
        )
        tables.append(
            TableResult(
                page=page,
                row_count=table.row_count,
                column_count=table.column_count,
                cells=cells,
            )
        )
    return TableExtractionResult(
        provider="azure-ai-documentintelligence", tables=tables, raw=result
    )
