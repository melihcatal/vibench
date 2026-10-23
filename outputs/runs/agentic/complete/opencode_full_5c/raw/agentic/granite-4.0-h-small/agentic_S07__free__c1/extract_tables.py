# [SAME-SCENARIO] extract_tables.py
"""Extract tables (cells and row structure) from documents using AWS Textract"""

from typing import BinaryIO, Dict, Any
import boto3
from botocore.exceptions import ClientError

# Load configuration from environment or local helper if needed
AWS_REGION = "us-east-1"


def extract_tables_from_image(image_bytes: bytes) -> Dict[str, Any]:
    """Extract tables from a document image using AWS Textract

    Args:
        image_bytes: Binary content of the scanned document (PNG/JPEG).

    Returns:
        Dict containing the Textract tables JSON response.
    """
    textract = boto3.client(service_name="textract", region_name=AWS_REGION)
    try:
        response = textract.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
        )
    except ClientError as e:
        raise RuntimeError(f"AWS Textract error: {e}")
    return response


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python extract_tables.py <path-to-image>")
        sys.exit(1)
    with open(sys.argv[1], "rb") as img:
        result = extract_tables_from_image(img.read())
    print(result)
