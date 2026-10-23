
import os
from document_client import get_document_intelligence_client
from document_models import ExtractedTable

def extract_tables_from_document(document_url: str) -> list[ExtractedTable]:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-layout", document_url
    )
    result = poller.result()

    extracted_tables = []
    for table in result.tables:
        cells_data = []
        for cell in table.cells:
            cells_data.append({
                "content": cell.content,
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "row_span": cell.row_span,
                "column_span": cell.column_span,
            })
        extracted_tables.append(
            ExtractedTable(cells=cells_data, rows=table.row_count, columns=table.column_count)
        )

    return extracted_tables
