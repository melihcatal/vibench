from typing import List
from azure.ai.documentintelligence import DocumentIntelligenceClient
from document_client import get_document_intelligence_client
from document_models import ExtractedTable

def extract_tables_from_url(url: str) -> List[ExtractedTable]:
    """
    Extracts tables from a document at a given URL using Azure Document Intelligence.

    Args:
        url: The URL of the document to analyze.

    Returns:
        A list of ExtractedTable objects.
    """
    document_intelligence_client = get_document_intelligence_client()
    
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", {"urlSource": url}
    )
    result = poller.result()
    
    extracted_tables = []
    if result.tables:
        for table in result.tables:
            cells = [
                {
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "content": cell.content,
                }
                for cell in table.cells
            ]
            extracted_tables.append(
                ExtractedTable(
                    row_count=table.row_count,
                    column_count=table.column_count,
                    cells=cells,
                )
            )
    return extracted_tables
