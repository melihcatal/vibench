# [SAME-SCENARIO] extract_text.py
"""Extract plain text from scanned document images using AWS Textract"""

from typing import BinaryIO, Dict, Any
import boto3
from botocore.exceptions import ClientError

# Load configuration from environment or local helper if needed
AWS_REGION = "us-east-1"


def extract_text_from_image(image_bytes: bytes) -> Dict[str, Any]:
    """Extract plain text from a document image using AWS Textract

    Args:
        image_bytes: Binary content of the scanned document (PNG/JPEG).

    Returns:
        Dict containing the Textract JSON response.
    """
    textract = boto3.client(service_name="textract", region_name=AWS_REGION)
    try:
        response = textract.detect_document_text(Document={"Bytes": image_bytes})
    except ClientError as e:
        raise RuntimeError(f"AWS Textract error: {e}")
    return response


if __name__ == "__main__":
    import sys

    # Simple CLI for testing
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <path-to-image>")
        sys.exit(1)
    with open(sys.argv[1], "rb") as img:
        result = extract_text_from_image(img.read())
    print(result)
