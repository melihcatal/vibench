import os
import boto3
from aws_encryption_sdk import KMSMasterKeyProvider

# SAME-SCENARIO: extract_tables.py

# Provider: Amazon Textract
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


def extract_tables_from_image(image_bytes):
    """Extract table structures and cells from a scanned document image using Amazon Textract.

    Args:
        image_bytes (bytes): Binary content of the scanned image.

    Returns:
        list: List of table objects with rows and cells.
    """
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )
    tables = []
    for item in response.get("Blocks", []):
        if item.get("BlockType") == "TABLE":
            table = {"rows": []}
            for inner_item in response.get("Blocks", []):
                if inner_item.get("BlockType") == "CELL" and inner_item.get(
                    "Relationships"
                ):
                    for rel in inner_item.get("Relationships", []):
                        if rel.get("Ids"):
                            cell = {
                                "row_index": inner_item.get("RowIndex"),
                                "col_index": inner_item.get("ColumnIndex"),
                                "content": "",
                            }
                            table["rows"].append(cell)
            tables.append(table)
    return tables
