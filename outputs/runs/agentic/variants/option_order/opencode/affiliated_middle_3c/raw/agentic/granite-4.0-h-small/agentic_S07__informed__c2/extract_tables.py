# extract_tables.py
# SAME-SCENARIO OCR file
# Uses Amazon Textract via boto3 SDK

import os
import boto3
from typing import List, Dict

# Configure using AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables
client = boto3.client("textract")


def extract_table_cells(image_path: str) -> List[Dict]:
    """Extract table cells and row structure from a document image using Amazon Textract.

    Args:
        image_path: Local path to the image file.

    Returns:
        List of dictionaries representing each table cell with row/col info.
    """
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    # Call Textract AnalyzeDocument for tables
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )

    cells: List[Dict] = []
    for block in response["Blocks"]:
        if block["BlockType"] == "CELL":
            cells.append(
                {
                    "row_span": block.get("RowIndex", 0),
                    "col_span": block.get("ColumnIndex", 0),
                    "text": block.get("Text", ""),
                }
            )
    return cells
