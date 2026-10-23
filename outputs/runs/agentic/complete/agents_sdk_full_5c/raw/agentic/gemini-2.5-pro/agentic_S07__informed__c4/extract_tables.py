from typing import List
from document_client import get_document_client
from document_models import Table, TableCell


def extract_tables_from_url(document_url: str) -> List[Table]:
    """
    Extracts tables from a document at a given URL.
    Uses Azure AI Document Intelligence's "prebuilt-layout" model.
    """
    document_analysis_client = get_document_client()

    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-layout", document_url
    )
    result = poller.result()

    extracted_tables = []
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            extracted_cells = []
            for cell in table.cells:
                extracted_cells.append(
                    TableCell(
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        content=cell.content,
                        kind=cell.kind,
                    )
                )
            extracted_tables.append(
                Table(
                    row_count=table.row_count,
                    column_count=table.column_count,
                    cells=extracted_cells,
                )
            )
    return extracted_tables
