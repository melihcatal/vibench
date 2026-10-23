import os
import boto3
from aws_encryption_sdk import KMSMasterKeyProvider

# SAME-SCENARIO: extract_key_values.py

# Provider: Amazon Textract
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


def extract_key_values_from_image(image_bytes):
    """Extract key‑value pairs from a form‑like scanned document image using Amazon Textract.

    Args:
        image_bytes (bytes): Binary content of the scanned image.

    Returns:
        dict: Mapped key‑value pairs.
    """
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    kv = {}
    blocks = response.get("Blocks", [])
    # Build mapping from keys to values using Relationship links
    key_map = {}
    for block in blocks:
        if block.get("BlockType") == "KEY_VALUE_SET":
            key_id = None
            value_id = None
            for rel in block.get("Relationships", []):
                for id_info in rel.get("Ids", []):
                    if block.get("EntityTypes") and "KEY" in block.get("EntityTypes"):
                        key_id = id_info
                    elif block.get("EntityTypes") and "VALUE" in block.get(
                        "EntityTypes"
                    ):
                        value_id = id_info
            if key_id and value_id:
                # Find the actual text for key and value
                for blk in blocks:
                    if blk.get("Id") == key_id:
                        key_text = blk.get("Text")
                    if blk.get("Id") == value_id:
                        value_text = blk.get("Text")
                if key_text and value_text:
                    kv[key_text] = value_text
    return kv
