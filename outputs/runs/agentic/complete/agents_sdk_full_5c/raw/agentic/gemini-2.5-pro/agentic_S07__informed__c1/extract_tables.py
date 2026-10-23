from document_client import get_document_client
from document_models import ExtractedTable, TableCell
from azure.ai.documentintelligence.models import AnalyzeResult
from typing import List

def extract_tables_from_url(document_url: str) -> List[ExtractedTable]:
    """
    Extracts tables from a document at a given URL using Azure Document Intelligence.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        A list of ExtractedTable objects found in the document.
    """
    client = get_document_client()

    poller = client.begin_analyze_document_from_url(
        model_id="prebuilt-layout",
        url=document_url
    )
    result: AnalyzeResult = poller.result()

    extracted_tables = []
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            cells = []
            for cell in table.cells:
                table_cell = TableCell(
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    content=cell.content,
                    kind=cell.kind if cell.kind else "content"
                )
                cells.append(table_cell)
            
            extracted_table = ExtractedTable(
                row_count=table.row_count,
                column_count=table.column_count,
                cells=cells
            )
            extracted_tables.append(extracted_table)
            
    return extracted_tables
