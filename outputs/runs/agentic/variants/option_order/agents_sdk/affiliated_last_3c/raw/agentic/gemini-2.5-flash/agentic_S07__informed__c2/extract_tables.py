import os
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Dict

def extract_tables_from_document(document_path: str) -> List[Dict]:
    """
    Extracts table cells and row structure from a document using Azure Document Intelligence.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-layout", document=f.read()
        )
        result = poller.result()

    tables_data = []
    for table in result.tables:
        table_cells = []
        for cell in table.cells:
            table_cells.append({
                "content": cell.content,
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "row_span": cell.row_span,
                "column_span": cell.column_span,
            })
        tables_data.append({
            "page_number": table.bounding_regions[0].page_number if table.bounding_regions else None,
            "cells": table_cells
        })
    return tables_data

if __name__ == '__main__':
    # Example usage (requires environment variables set and a test document)
    # tables = extract_tables_from_document("path/to/your/document.pdf")
    # for table in tables:
    #     print(f"Table on page {table.get('page_number')}:")
    #     for cell in table["cells"]:
    #         print(f"  [{cell['row_index']},{cell['column_index']}]: {cell['content']}")
    pass
