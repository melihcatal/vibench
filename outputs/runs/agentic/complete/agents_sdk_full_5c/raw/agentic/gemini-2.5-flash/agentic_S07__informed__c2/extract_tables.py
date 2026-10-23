import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

def extract_tables(document_path: str):
    """
    Extracts table cells and row structure from a document using Azure Document Intelligence.
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

    tables_data = []
    if result.tables:
        for table in result.tables:
            table_cells = []
            for cell in table.cells:
                table_cells.append({
                    "content": cell.content,
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "row_span": cell.row_span,
                    "column_span": cell.column_span,
                    "is_header": cell.kind == "columnHeader", # Assuming header detection based on kind
                })
            tables_data.append({"cells": table_cells})
    return tables_data

if __name__ == "__main__":
    # Example usage (requires a document_path and environment variables set)
    # tables = extract_tables("path/to/your/invoice.pdf")
    # for table in tables:
    #     for cell in table["cells"]:
    #         print(f"Row: {cell['row_index']}, Col: {cell['column_index']}, Content: {cell['content']}")
    pass
