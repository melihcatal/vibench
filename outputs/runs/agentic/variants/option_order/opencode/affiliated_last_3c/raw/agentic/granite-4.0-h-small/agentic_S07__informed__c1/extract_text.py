import os
from boto3 import client

# Amazon Textract integration
# Provider identifiable by 'boto3' import and 'textract' client

# Load AWS credentials from environment variables (expected to be set)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract plain text from a scanned document image using Amazon Textract.

    Args:
        image_bytes: Binary content of the image.

    Returns:
        Extracted plain text.
    """
    textract = client(
        "textract",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = textract.detect_document_text(Document={"Bytes": image_bytes})
    # Gather text from blocks
    text = " ".join(
        item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"
    )
    return text
