import os
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import normalize_textract_response, Table, TableCell


def extract_tables(
    image_path: str, region: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Extract table cells and row structure from a document using Amazon Textract.

    Args:
        image_path: Path to the image file
        region: AWS region (defaults to AWS_DEFAULT_REGION env var)

    Returns:
        List of tables with cell data
    """
    # Read image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Initialize Textract client
    client = DocumentClient(region_name=region)

    # Call Textract API with table analysis
    response = client.analyze_document(image_bytes, feature_types=["TABLES"])

    # Normalize response
    result = normalize_textract_response(response)

    # Convert tables to dict format
    tables_data = []

    for table in result.tables:
        # Create 2D array for table cells
        cell_grid = [
            [None for _ in range(table.column_count)] for _ in range(table.row_count)
        ]

        # Fill the grid
        for cell in table.cells:
            if (
                0 <= cell.row_index - 1 < table.row_count
                and 0 <= cell.column_index - 1 < table.column_count
            ):
                cell_grid[cell.row_index - 1][cell.column_index - 1] = {
                    "text": cell.text,
                    "confidence": cell.confidence,
                    "geometry": cell.geometry,
                }

        tables_data.append(
            {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": cell_grid,
                "geometry": table.geometry,
            }
        )

    return tables_data
