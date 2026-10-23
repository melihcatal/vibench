import os
from typing import Optional
from document_client import DocumentClient
from document_models import normalize_textract_response


def extract_text(image_path: str, region: Optional[str] = None) -> str:
    """Extract plain text from a scanned document image using Amazon Textract.

    Args:
        image_path: Path to the image file
        region: AWS region (defaults to AWS_DEFAULT_REGION env var)

    Returns:
        Extracted text as a single string
    """
    # Read image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Initialize Textract client
    client = DocumentClient(region_name=region)

    # Call Textract API
    response = client.detect_document_text(image_bytes)

    # Extract text from response
    blocks = response.get("Blocks", [])
    text_lines = []

    for block in blocks:
        if block.get("BlockType") == "LINE":
            text = block.get("Text", "")
            if text:
                text_lines.append(text)

    return "\n".join(text_lines)
