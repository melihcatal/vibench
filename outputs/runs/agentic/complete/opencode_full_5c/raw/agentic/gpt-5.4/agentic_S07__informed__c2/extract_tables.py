from __future__ import annotations

from document_client import get_document_intelligence_client, get_document_model_id
from document_models import (
    DocumentRequest,
    TableCell,
    TableExtractionResult,
    TableResult,
    as_dict,
)


def extract_tables(request: DocumentRequest) -> TableExtractionResult:
    client = get_document_intelligence_client()
    model_id = request.model_id or get_document_model_id("prebuilt-layout")
    poller = client.begin_analyze_document(
        model_id=model_id, body=request.file_bytes, locale=request.locale
    )
    result = poller.result()
    tables: list[TableResult] = []
    for table in result.tables or []:
        page_number = getattr((table.bounding_regions or [None])[0], "page_number", 1)
        cells = [
            TableCell(
                row_index=cell.row_index,
                column_index=cell.column_index,
                text=cell.content,
                row_span=getattr(cell, "row_span", 1) or 1,
                column_span=getattr(cell, "column_span", 1) or 1,
                kind=getattr(cell, "kind", None),
                confidence=getattr(cell, "confidence", None),
            )
            for cell in table.cells or []
        ]
        tables.append(
            TableResult(
                page_number=page_number,
                row_count=table.row_count,
                column_count=table.column_count,
                cells=cells,
            )
        )
    return TableExtractionResult(
        provider="azure-ai-documentintelligence",
        model_id=model_id,
        tables=tables,
        raw=as_dict(result),
    )
