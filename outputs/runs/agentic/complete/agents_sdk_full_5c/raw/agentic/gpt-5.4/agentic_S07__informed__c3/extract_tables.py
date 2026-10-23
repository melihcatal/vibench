from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_LAYOUT_MODEL, get_document_client
from document_models import TableCell, TableResponse


def extract_tables(document_path: str) -> TableResponse:
    client = get_document_client()
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=DEFAULT_LAYOUT_MODEL,
            body=AnalyzeDocumentRequest(bytes_source=f.read()),
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
                    content=cell.content or "",
                    row_span=cell.row_span or 1,
                    column_span=cell.column_span or 1,
                    page_number=(cell.bounding_regions[0].page_number if cell.bounding_regions else None),
                    kind=str(cell.kind) if getattr(cell, "kind", None) else None,
                )
            )
        tables.append(cells)
    return TableResponse(tables=tables, provider="azure-document-intelligence", model_id=DEFAULT_LAYOUT_MODEL)
