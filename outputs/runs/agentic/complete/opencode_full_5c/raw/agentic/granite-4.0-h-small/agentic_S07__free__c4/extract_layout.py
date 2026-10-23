import os
from document_client import DocumentClient


def extract_layout(image_path: str) -> dict:
    """Extract layout elements (blocks, lines, tables) from a document image using the AWS Textract provider.

    Args:
        image_path: Local path to the scanned document image.
    Returns:
        Dictionary containing layout elements (blocks, lines, tables) as returned by the provider.
    """
    client = DocumentClient(service="aws_textract")
    with open(image_path, "rb") as img_file:
        response = client.analyze_document(image_bytes=img_file.read())
    # Return the full structured response for downstream processing.
    return response
