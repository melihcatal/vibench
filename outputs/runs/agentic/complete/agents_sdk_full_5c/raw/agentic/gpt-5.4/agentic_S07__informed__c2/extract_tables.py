from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_LAYOUT_MODEL, get_document_client, load_document_bytes
from document_models import TableCellModel, TableModel, TablesResult


def extract_tables(document_path: str, model_id: str = DEFAULT_LAYOUT_MODEL) -> TablesResult:
    client = get_document_client()
    body = AnalyzeDocumentRequest(bytes_source=load_document_bytes(document_path))
    poller = client.begin_analyze_document(model_id=model_id, body=body)
    result = poller.result()

    tables = []
    for table in result.tables or []:
        cells = []
        for cell in table.cells or []:
            region = (getattr(cell, "bounding_regions", None) or [None])[0]
            cells.append(
                TableCellModel(
                    row_index=getattr(cell, "row_index", 0),
                    column_index=getattr(cell, "column_index", 0),
                    content=getattr(cell, "content", "") or "",
                    kind=getattr(cell, "kind", None),
                    row_span=getattr(cell, "row_span", 1) or 1,
                    column_span=getattr(cell, "column_span", 1) or 1,
                    page_number=getattr(region, "page_number", None) if region else None,
                )
            )
        tables.append(
            TableModel(
                row_count=getattr(table, "row_count", 0),
                column_count=getattr(table, "column_count", 0),
                cells=cells,
            )
        )

    return TablesResult(tables=tables, provider="azure-document-intelligence", model_id=model_id)
