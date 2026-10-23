from typing import List
from document_client import get_document_client
from document_models import DocumentTable


def extract_tables_from_document(file_path: str) -> List[DocumentTable]:
    document_intelligence_client = get_document_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    tables = []
    if result.tables:
        for table in result.tables:
            cells = []
            for cell in table.cells:
                cells.append(
                    {
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "content": cell.content,
                    }
                )
            tables.append(
                DocumentTable(
                    row_count=table.row_count,
                    column_count=table.column_count,
                    cells=cells,
                )
            )
    return tables
