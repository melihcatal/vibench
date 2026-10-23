from typing import List
from document_client import get_document_analysis_client
from document_models import Table, TableCell


def extract_tables_from_document(file_path: str = None, url: str = None) -> List[Table]:
    client = get_document_analysis_client()

    poller = None
    if url:
        poller = client.begin_analyze_document("prebuilt-layout", {"urlSource": url})
    elif file_path:
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-layout", f.read())
    else:
        raise ValueError("Either file_path or url must be provided.")

    result = poller.result()

    extracted_tables = []
    if result.tables:
        for table in result.tables:
            cells = []
            for cell in table.cells:
                cells.append(
                    TableCell(
                        content=cell.content,
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        row_span=cell.row_span if cell.row_span else 1,
                        column_span=cell.column_span if cell.column_span else 1,
                    )
                )
            extracted_tables.append(
                Table(
                    cells=cells,
                    row_count=table.row_count,
                    column_count=table.column_count,
                )
            )
    return extracted_tables
