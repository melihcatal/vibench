from typing import List, Dict, Any
from document_client import get_document_client

def extract_tables_from_url(document_url: str) -> List[Dict[str, Any]]:
    """
    Extracts table structures from a document at a given URL.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        A list of dictionaries, each representing a table with its cells.
    """
    document_client = get_document_client()

    poller = document_client.begin_analyze_document(
        "prebuilt-layout", {"urlSource": document_url}
    )
    result = poller.result()
    
    extracted_tables = []
    if result.tables:
        for table in result.tables:
            table_data = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": [
                    {
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "content": cell.content,
                        "kind": cell.kind,
                    }
                    for cell in table.cells
                ],
            }
            extracted_tables.append(table_data)

    return extracted_tables
