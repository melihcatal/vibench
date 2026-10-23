import os
import json
import base64
from typing import List, Dict, Any, Optional
import requests


def extract_tables_from_image(
    image_path: str, include_cells: bool = True
) -> List[Dict[str, Any]]:
    """
    Extract table cells and row structure from a document using Amazon Textract.

    Args:
        image_path: Path to the image file
        include_cells: Whether to include detailed cell information

    Returns:
        List of tables with their structure
    """
    import boto3
    from botocore.exceptions import ClientError

    client = boto3.client(
        "textract",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "your-access-key"),
        aws_secret_access_key=os.environ.get(
            "AWS_SECRET_ACCESS_KEY", "your-secret-key"
        ),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )

    tables = []

    blocks = response.get("Blocks", [])

    table_blocks = [block for block in blocks if block["BlockType"] == "TABLE"]

    for table_block in table_blocks:
        table_data = {
            "id": table_block["Id"],
            "confidence": table_block.get("Confidence", 0),
            "geometry": table_block.get("Geometry", {}),
            "relationships": table_block.get("Relationships", []),
            "rows": [],
            "cells": [],
        }

        cell_relationships = []
        for relationship in table_block.get("Relationships", []):
            if relationship["Type"] == "CHILD":
                cell_relationships.extend(relationship.get("Ids", []))

        cells = []
        for cell_id in cell_relationships:
            cell_block = next((b for b in blocks if b["Id"] == cell_id), None)
            if cell_block and cell_block["BlockType"] == "CELL":
                cell_info = {
                    "id": cell_block["Id"],
                    "row_index": cell_block.get("RowIndex", 0),
                    "column_index": cell_block.get("ColumnIndex", 0),
                    "row_span": cell_block.get("RowSpan", 1),
                    "column_span": cell_block.get("ColumnSpan", 1),
                    "confidence": cell_block.get("Confidence", 0),
                    "geometry": cell_block.get("Geometry", {}),
                    "text": "",
                }

                cell_child_rels = []
                for rel in cell_block.get("Relationships", []):
                    if rel["Type"] == "CHILD":
                        cell_child_rels.extend(rel.get("Ids", []))

                cell_text_parts = []
                for child_id in cell_child_rels:
                    child_block = next((b for b in blocks if b["Id"] == child_id), None)
                    if child_block and child_block["BlockType"] == "WORD":
                        cell_text_parts.append(child_block.get("Text", ""))

                cell_info["text"] = " ".join(cell_text_parts)
                cells.append(cell_info)

        if include_cells:
            table_data["cells"] = cells

        max_row = max([cell["row_index"] for cell in cells]) if cells else 0
        max_col = max([cell["column_index"] for cell in cells]) if cells else 0

        table_data["dimensions"] = {"rows": max_row, "columns": max_col}

        tables.append(table_data)

    return tables


def extract_tables_from_bytes(image_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extract tables from image bytes using Amazon Textract.

    Args:
        image_bytes: Raw image bytes

    Returns:
        List of tables with their structure
    """
    import boto3
    from botocore.exceptions import ClientError

    client = boto3.client(
        "textract",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "your-access-key"),
        aws_secret_access_key=os.environ.get(
            "AWS_SECRET_ACCESS_KEY", "your-secret-key"
        ),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )

    tables = []

    blocks = response.get("Blocks", [])

    table_blocks = [block for block in blocks if block["BlockType"] == "TABLE"]

    for table_block in table_blocks:
        table_data = {
            "id": table_block["Id"],
            "confidence": table_block.get("Confidence", 0),
            "geometry": table_block.get("Geometry", {}),
            "relationships": table_block.get("Relationships", []),
            "cells": [],
        }

        cell_relationships = []
        for relationship in table_block.get("Relationships", []):
            if relationship["Type"] == "CHILD":
                cell_relationships.extend(relationship.get("Ids", []))

        cells = []
        for cell_id in cell_relationships:
            cell_block = next((b for b in blocks if b["Id"] == cell_id), None)
            if cell_block and cell_block["BlockType"] == "CELL":
                cell_info = {
                    "id": cell_block["Id"],
                    "row_index": cell_block.get("RowIndex", 0),
                    "column_index": cell_block.get("ColumnIndex", 0),
                    "row_span": cell_block.get("RowSpan", 1),
                    "column_span": cell_block.get("ColumnSpan", 1),
                    "confidence": cell_block.get("Confidence", 0),
                    "geometry": cell_block.get("Geometry", {}),
                    "text": "",
                }

                cell_child_rels = []
                for rel in cell_block.get("Relationships", []):
                    if rel["Type"] == "CHILD":
                        cell_child_rels.extend(rel.get("Ids", []))

                cell_text_parts = []
                for child_id in cell_child_rels:
                    child_block = next((b for b in blocks if b["Id"] == child_id), None)
                    if child_block and child_block["BlockType"] == "WORD":
                        cell_text_parts.append(child_block.get("Text", ""))

                cell_info["text"] = " ".join(cell_text_parts)
                cells.append(cell_info)

        table_data["cells"] = cells

        tables.append(table_data)

    return tables
