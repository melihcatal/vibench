import os
from boto3 import client

# Amazon Textract integration for layout extraction
# Provider identifiable by 'boto3' import and 'textract' client

# Load AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def extract_layout_from_image(image_bytes: bytes) -> dict:
    """Extract layout elements (blocks, lines, tables) from a document image using Amazon Textract.

    Args:
        image_bytes: Binary content of the scanned image.

    Returns:
        Dictionary representing layout hierarchy.
    """
    textract = client(
        "textract",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )  # Enable layout/features
    # Simple normalization: group by block type
    layout = {"lines": [], "tables": [], "other": []}
    for item in response.get("Blocks", []):
        block_type = item.get("BlockType")
        if block_type == "LINE":
            layout["lines"].append(item.get("Text"))
        elif block_type == "TABLE":
            layout["tables"].append(item)
        else:
            layout["other"].append(item)
    return layout
