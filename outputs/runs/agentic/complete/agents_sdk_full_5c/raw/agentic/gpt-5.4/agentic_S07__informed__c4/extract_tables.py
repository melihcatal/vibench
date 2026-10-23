from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_document_intelligence_client, guess_content_type, read_bytes
from document_models import TableCell, TableResult, normalize_text


def extract_tables(document_path: str) -> TableResult:
    client = get_document_intelligence_client()
    payload = read_bytes(document_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=AnalyzeDocumentRequest(bytes_source=payload),
        content_type=guess_content_type(document_path),
    )
    result = poller.result()

    tables = []
    for table in result.tables or []:
        cells = []
        for cell in table.cells or []:
            page_number = None
            if cell.bounding_regions:
                page_number = cell.bounding_regions[0].page_number
            cells.append(
                TableCell(
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    text=normalize_text(cell.content),
                    row_span=cell.row_span or 1,
                    column_span=cell.column_span or 1,
                    confidence=None,
                    page=page_number,
                )
            )
        tables.append(cells)

    return TableResult(
        tables=tables,
        provider="azure-ai-documentintelligence:prebuilt-layout",
        raw=result,
    )
