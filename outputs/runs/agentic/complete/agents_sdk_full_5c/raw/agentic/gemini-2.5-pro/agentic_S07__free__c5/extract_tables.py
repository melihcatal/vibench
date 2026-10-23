# extract_tables.py
from typing import List
from document_client import get_document_intelligence_client
from document_models import ExtractedTable, TableCell

def extract_tables_from_url(document_url: str) -> List[ExtractedTable]:
    """
    Extracts tables from a document image using Azure AI Document Intelligence.
    This uses the "prebuilt-layout" model which includes table detection.
    """
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-layout", analyze_request={"urlSource": document_url}
    )
    result = poller.result()

    extracted_tables: List[ExtractedTable] = []
    if result.tables:
        for table in result.tables:
            cells = []
            for cell in table.cells:
                cells.append(
                    TableCell(
                        content=cell.content,
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        is_header=(cell.kind == "columnHeader" or cell.kind == "rowHeader"),
                    )
                )
            extracted_tables.append(
                ExtractedTable(
                    cells=cells,
                    row_count=table.row_count,
                    column_count=table.column_count,
                )
            )

    return extracted_tables
