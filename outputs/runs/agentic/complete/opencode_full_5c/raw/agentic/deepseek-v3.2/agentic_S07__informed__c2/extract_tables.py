import os
from typing import List, Dict, Any
from document_client import DocumentClient
from document_models import Table, TableCell, TextractResponseParser


def extract_tables_from_document(image_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extract table cells and row structure from a document using Amazon Textract.

    Args:
        image_bytes: Bytes of the document image

    Returns:
        List of extracted tables
    """
    # Initialize Textract client
    client = DocumentClient()

    # Call Textract AnalyzeDocument API with TABLES feature
    response = client.analyze_document(
        document_bytes=image_bytes, feature_types=["TABLES"]
    )

    # Parse tables from response
    tables = TextractResponseParser.parse_tables(response)

    # Convert to dictionary format
    result = []
    for table in tables:
        table_dict = {
            "row_count": table.row_count,
            "column_count": table.column_count,
            "confidence": table.confidence,
            "cells": [],
        }

        # Organize cells by row and column
        for cell in table.cells:
            cell_dict = {
                "text": cell.text,
                "row": cell.row_index,
                "column": cell.column_index,
                "row_span": cell.row_span,
                "column_span": cell.column_span,
                "confidence": cell.confidence,
            }
            table_dict["cells"].append(cell_dict)

        result.append(table_dict)

    return result


def extract_tables_with_structure(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract tables with complete structure including headers and data cells.

    Args:
        image_bytes: Bytes of the document image

    Returns:
        Complete table structure
    """
    client = DocumentClient()

    # Use TABLES feature for table extraction
    response = client.analyze_document(
        document_bytes=image_bytes, feature_types=["TABLES"]
    )

    tables = TextractResponseParser.parse_tables(response)

    structured_tables = []
    for table_idx, table in enumerate(tables):
        # Create 2D array representation
        table_grid = [
            [None for _ in range(table.column_count)] for _ in range(table.row_count)
        ]

        for cell in table.cells:
            # Fill cells in the grid
            for r in range(cell.row_span):
                for c in range(cell.column_span):
                    row_idx = cell.row_index + r - 1  # Textract uses 1-based indexing
                    col_idx = cell.column_index + c - 1
                    if (
                        0 <= row_idx < table.row_count
                        and 0 <= col_idx < table.column_count
                    ):
                        table_grid[row_idx][col_idx] = cell.text

        # Identify potential headers (first row)
        headers = []
        if table_grid:
            headers = [
                cell if cell else f"Column_{i + 1}"
                for i, cell in enumerate(table_grid[0])
            ]

        structured_tables.append(
            {
                "table_index": table_idx,
                "dimensions": {"rows": table.row_count, "columns": table.column_count},
                "headers": headers,
                "data": table_grid[1:] if table_grid else [],  # Exclude header row
                "confidence": table.confidence,
                "total_cells": len(table.cells),
            }
        )

    return {
        "tables": structured_tables,
        "total_tables": len(tables),
        "provider": "Amazon Textract",
    }
