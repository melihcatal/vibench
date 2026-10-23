import os
from boto3 import client

# Amazon Textract for key-value pair extraction
# Provider identifiable by 'boto3' import and 'textract' client

# Load AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def extract_key_values_from_image(image_bytes: bytes) -> dict:
    """Extract key-value pairs from a form-like document using Amazon Textract.

    Args:
        image_bytes: Binary content of the scanned image.

    Returns:
        Dictionary mapping keys to values.
    """
    textract = client(
        "textract",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    kv = {}
    # Textract returns relationships; simplify by pairing KEY with VALUE
    for item in response.get("Blocks", []):
        if item.get("BlockType") == "KEY_VALUE_SET":
            rel = item.get("Relationships", [])
            key = None
            value = None
            for rel_item in rel:
                if rel_item.get("Type") == "KEY":
                    for k in rel_item.get("Ids", []):
                        blk = next(
                            (b for b in response["Blocks"] if b["Id"] == k), None
                        )
                        if blk and blk.get("BlockType") == "KEY_VALUE_SET":
                            key = blk.get("Text")
                elif rel_item.get("Type") == "VALUE":
                    for v in rel_item.get("Ids", []):
                        blk = next(
                            (b for b in response["Blocks"] if b["Id"] == v), None
                        )
                        if blk and blk.get("BlockType") == "KEY_VALUE_SET":
                            value = blk.get("Text")
            if key and value:
                kv[key] = value
    return kv
