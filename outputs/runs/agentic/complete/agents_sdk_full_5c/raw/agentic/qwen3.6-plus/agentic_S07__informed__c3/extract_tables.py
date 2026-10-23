"""
Extract table cells and row structure from a document using Azure AI Document Intelligence.

Uses the azure-ai-documentintelligence SDK with the prebuilt-layout model to
detect tables and their cell-level structure, including row/column indices,
spans, and cell content.
"""

from typing import Optional

from document_client import create_document_intelligence_client, read_file_bytes
from document_models import OcrTableResponse, normalize_azure_di_table_response


def extract_tables_from_document(
    file_path: str,
    *,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> OcrTableResponse:
    """
    Extract table structures from a document using Azure Document Intelligence.

    Args:
        file_path: Path to the local document file.
        endpoint: Azure DI endpoint URL. Falls back to AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT.
        key: Azure DI API key. Falls back to AZURE_DOCUMENT_INTELLIGENCE_KEY.

    Returns:
        OcrTableResponse containing table data with cell-level detail.
    """
    client = create_document_intelligence_client(endpoint=endpoint, key=key)
    file_bytes = read_file_bytes(file_path)

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=file_bytes,
    )
    result = poller.result()
    result_dict = result.as_dict()

    return normalize_azure_di_table_response(result_dict)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        resp = extract_tables_from_document(sys.argv[1])
        for idx, table in enumerate(resp.tables):
            print(f"Table {idx}: {table.row_count} rows x {table.column_count} columns")
            for cell in table.cells:
                print(f"  [{cell.row_index},{cell.column_index}] {cell.content}")
    else:
        print("Usage: python extract_tables.py <path-to-document>")
