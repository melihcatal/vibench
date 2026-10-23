import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

def extract_layout_elements(document_path: str):
    """
    Extracts layout elements (paragraphs, tables, etc.) from a document
    using Azure Document Intelligence.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set.")

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
        )
        result: AnalyzeResult = poller.result()

    layout_data = {
        "paragraphs": [p.content for p in result.paragraphs] if result.paragraphs else [],
        "tables": [
            {
                "cells": [
                    {"content": cell.content, "row_index": cell.row_index, "column_index": cell.column_index}
                    for cell in table.cells
                ]
            }
            for table in result.tables
        ] if result.tables else [],
        "styles": [s.is_handwritten for s in result.styles] if result.styles else [],
    }
    return layout_data

if __name__ == "__main__":
    # Example usage (requires a document_path and environment variables set)
    # layout = extract_layout_elements("path/to/your/document.pdf")
    # print(layout)
    pass
