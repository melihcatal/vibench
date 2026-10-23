"""
Extracts table cells and row structure from a document using Azure AI Document Intelligence.
Uses the 'prebuilt-layout' model to detect tables and parse cell content with row/column indexing.
"""

import os
from typing import List

from document_client import (
    create_document_client,
    read_image_bytes,
    normalize_azure_poller_response,
)
from document_models import (
    TableData,
    TableCell,
    normalize_table_result,
)

# Azure Document Intelligence prebuilt-layout model identifier for table extraction
AZURE_TABLE_MODEL_ID = "prebuilt-layout"


def extract_tables_from_image(
    file_path: str,
    model_id: str = AZURE_TABLE_MODEL_ID,
) -> List[TableData]:
    """
    Extract tables with cell and row structure from a document image using Azure AI Document Intelligence.

    Args:
        file_path: Path to the document image or PDF file.
        model_id: Azure Document Intelligence model ID. Defaults to 'prebuilt-layout'.

    Returns:
        List[TableData]: List of extracted tables with cells, row/column indices, and spans.

    Raises:
        ValueError: If required Azure environment variables are not set.
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Document file not found: {file_path}")

    file_bytes = read_image_bytes(file_path)
    client = create_document_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"base64Source": file_bytes.hex()},
    )

    result = normalize_azure_poller_response(poller)
    tables = normalize_table_result(result)
    return tables


def extract_tables_from_bytes(
    file_bytes: bytes,
    model_id: str = AZURE_TABLE_MODEL_ID,
) -> List[TableData]:
    """
    Extract tables from document bytes using Azure AI Document Intelligence.

    Args:
        file_bytes: Raw bytes of the document file.
        model_id: Azure Document Intelligence model ID. Defaults to 'prebuilt-layout'.

    Returns:
        List[TableData]: List of extracted tables with cells and row structure.
    """
    client = create_document_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"base64Source": file_bytes.hex()},
    )

    result = normalize_azure_poller_response(poller)
    tables = normalize_table_result(result)
    return tables


def tables_to_csv(tables: List[TableData]) -> List[str]:
    """
    Convert extracted tables to CSV format strings.

    Args:
        tables: List of TableData objects from extract_tables_from_image.

    Returns:
        List[str]: CSV-formatted string for each table.
    """
    csv_outputs = []

    for table in tables:
        # Build a grid
        grid = [["" for _ in range(table.column_count)] for _ in range(table.row_count)]
        for cell in table.cells:
            for r in range(cell.row_index, cell.row_index + cell.row_span):
                for c in range(cell.column_index, cell.column_index + cell.column_span):
                    if r < table.row_count and c < table.column_count:
                        grid[r][c] = cell.content

        # Convert grid to CSV
        lines = []
        for row in grid:
            escaped = ['"' + val.replace('"', '""') + '"' if ',' in val or '"' in val else val for val in row]
            lines.append(",".join(escaped))
        csv_outputs.append("\n".join(lines))

    return csv_outputs
