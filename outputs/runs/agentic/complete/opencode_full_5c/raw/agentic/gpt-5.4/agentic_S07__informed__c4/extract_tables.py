from __future__ import annotations

from document_client import (
    DEFAULT_LAYOUT_MODEL,
    get_document_intelligence_client,
    resolve_model_id,
)
from document_models import (
    DocumentRequest,
    TableCell,
    TableResult,
    TablesExtractionResult,
    normalize_text,
)


def extract_tables(request: DocumentRequest) -> TablesExtractionResult:
    client = get_document_intelligence_client()
    model_id = resolve_model_id(request.model_id, DEFAULT_LAYOUT_MODEL)
    poller = client.begin_analyze_document(
        model_id=model_id,
        body=request.document_bytes,
        content_type=request.mime_type,
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
                    content=normalize_text(cell.content),
                    row_span=cell.row_span or 1,
                    column_span=cell.column_span or 1,
                    kind=cell.kind or "content",
                )
            )
        page = table.bounding_regions[0].page_number if table.bounding_regions else 1
        tables.append(
            TableResult(
                page=page,
                row_count=table.row_count,
                column_count=table.column_count,
                cells=cells,
            )
        )
    return TablesExtractionResult(
        provider="azure-document-intelligence",
        tables=tables,
        raw=result,
    )
