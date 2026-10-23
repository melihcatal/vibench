import os
import boto3
from aws_encryption_sdk import KMSMasterKeyProvider

# SAME-SCENARIO: extract_layout.py

# Provider: Amazon Textract
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


def extract_layout_from_image(image_bytes):
    """Extract layout elements (blocks, lines, tables) from a scanned document image using Amazon Textract.

    Args:
        image_bytes (bytes): Binary content of the scanned image.

    Returns:
        dict: Layout information containing blocks, lines, and tables.
    """
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    layout = {"blocks": [], "lines": [], "tables": []}
    for item in response.get("Blocks", []):
        if item.get("BlockType") == "LINE":
            layout["lines"].append(item.get("Text"))
        elif item.get("BlockType") == "TABLE":
            layout["tables"].append(item)
        else:
            layout["blocks"].append(item)
    return layout
