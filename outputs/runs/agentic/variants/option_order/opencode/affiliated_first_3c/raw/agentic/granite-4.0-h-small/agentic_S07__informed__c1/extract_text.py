import os
import boto3
from aws_encryption_sdk import KMSMasterKeyProvider

# SAME-SCENARIO: extract_text.py

# Provider: Amazon Textract
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


def extract_text_from_image(image_bytes):
    """Extract plain text from a scanned document image using Amazon Textract.

    Args:
        image_bytes (bytes): Binary content of the scanned image.

    Returns:
        str: Extracted plain text.
    """
    textract = boto3.client("textract")
    # Call DetectDocumentText API
    response = textract.detect_document_text(Document={"Bytes": image_bytes})
    text = ""
    for item in response.get("Blocks", []):
        if item.get("BlockType") == "LINE":
            text += item.get("Text", "") + "\n"
    return text.strip()
