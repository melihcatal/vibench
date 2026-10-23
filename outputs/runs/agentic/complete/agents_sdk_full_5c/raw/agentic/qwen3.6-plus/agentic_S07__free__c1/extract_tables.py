"""
extract_tables.py - Extracts table cells and row structure from a document
using Azure AI Document Intelligence (prebuilt-layout model).

Provider: Azure AI Document Intelligence
SDK: azure-ai-formrecognizer
Model: prebuilt-layout
"""

from typing import List

from document_client import get_azure_client
from document_models import (
    BoundingBox,
    ExtractTablesRequest,
    ExtractTablesResponse,
    TableCell,
    TableData,
)

PROVIDER = "azure"
AZURE_MODEL_ID = "prebuilt-layout"


def _get_bounding_box(cell) -> BoundingBox:
    """Extract bounding box from a table cell."""
    if hasattr(cell, "bounding_regions") and cell.bounding_regions:
        region = cell.bounding_regions[0]
        if hasattr(region, "bounding_box") and region.bounding_box:
            bb = region.bounding_box
            return BoundingBox(
                x=bb[0] if len(bb) > 0 else 0.0,
                y=bb[1] if len(bb) > 1 else 0.0,
                width=(bb[2] - bb[0]) if len(bb) > 2 else 0.0,
                height=(bb[3] - bb[1]) if len(bb) > 3 else 0.0,
            )
    return BoundingBox()


def extract_tables(request: ExtractTablesRequest) -> ExtractTablesResponse:
    """
    Extract table structures (cells, rows, columns) from a document image
    using Azure AI Document Intelligence's prebuilt-layout model.

    Args:
        request: ExtractTablesRequest with image source.

    Returns:
        ExtractTablesResponse containing extracted TableData objects.
    """
    from io import BytesIO
    import base64

    if request.image.base64_data is None:
        raise ValueError("Image base64_data is required for table extraction.")

    image_bytes = BytesIO(base64.b64decode(request.image.base64_data))

    client = get_azure_client()
    analysis_client = client.create_document_analysis_client()

    poller = analysis_client.begin_analyze_document(
        model_id=AZURE_MODEL_ID,
        document=image_bytes,
    )
    result = poller.result()

    all_tables: List[TableData] = []

    for page in result.pages:
        if hasattr(page, "tables") and page.tables:
            for table in page.tables:
                table_id = f"page_{page.page_number}_table_{table.row_count}x{table.column_count}"
                cells: List[TableCell] = []

                if hasattr(table, "cells") and table.cells:
                    for cell in table.cells:
                        row_span = 1
                        col_span = 1
                        if hasattr(cell, "row_span"):
                            row_span = cell.row_span
                        if hasattr(cell, "column_span"):
                            col_span = cell.column_span

                        bbox = _get_bounding_box(cell)
                        cell_text = cell.content if hasattr(cell, "content") else ""

                        table_cell = TableCell(
                            text=cell_text,
                            row_index=cell.row_index if hasattr(cell, "row_index") else 0,
                            col_index=cell.column_index if hasattr(cell, "column_index") else 0,
                            row_span=row_span,
                            col_span=col_span,
                            confidence=cell.confidence if hasattr(cell, "confidence") else 0.0,
                            bounding_box=bbox,
                        )
                        cells.append(table_cell)

                table_data = TableData(
                    table_id=table_id,
                    rows=table.row_count if hasattr(table, "row_count") else 0,
                    columns=table.column_count if hasattr(table, "column_count") else 0,
                    cells=cells,
                    confidence=table.confidence if hasattr(table, "confidence") else 0.0,
                )
                all_tables.append(table_data)

    return ExtractTablesResponse(
        tables=all_tables,
        page_count=len(result.pages) if result.pages else 0,
        provider=PROVIDER,
        raw_response={"status": "success", "model_id": AZURE_MODEL_ID},
    )


def extract_tables_to_dicts(request: ExtractTablesRequest) -> List[List[dict]]:
    """
    Extract tables and convert each to a list of row dictionaries.

    Args:
        request: ExtractTablesRequest with image source.

    Returns:
        List of tables, each as a list of row dictionaries with column headers.
    """
    response = extract_tables(request)
    result_tables = []

    for table in response.tables:
        header_row = {}
        rows = []
        cell_map = {}

        for cell in table.cells:
            cell_map[(cell.row_index, cell.col_index)] = cell.text.strip()

        if table.rows > 0 and table.columns > 0:
            for col_idx in range(table.columns):
                header_text = cell_map.get((0, col_idx), f"col_{col_idx}")
                header_row[col_idx] = header_text

            for row_idx in range(1, table.rows):
                row = {}
                for col_idx in range(table.columns):
                    header = header_row.get(col_idx, f"col_{col_idx}")
                    row[header] = cell_map.get((row_idx, col_idx), "")
                rows.append(row)

        result_tables.append(rows)

    return result_tables


def extract_tables_from_file(file_path: str) -> ExtractTablesResponse:
    """
    Convenience function to extract tables directly from a file path.

    Args:
        file_path: Path to the document image file.

    Returns:
        ExtractTablesResponse with extracted table data.
    """
    from document_client import prepare_image_source

    image_source = prepare_image_source(file_path=file_path)
    req = ExtractTablesRequest(image=image_source)
    return extract_tables(req)
