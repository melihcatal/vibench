import os
from document_client import DocumentClient


def extract_text(image_path: str) -> str:
    """Extract plain text from a scanned document image using the Azure Computer Vision OCR provider.

    Args:
        image_path: Path to the local image file.
    Returns:
        Extracted plain text as a string.
    """
    client = DocumentClient(service="azure_ocr")
    # Azure Computer Vision expects a byte stream; we read the file locally.
    with open(image_path, "rb") as img_file:
        result = client.ocr_image(image_bytes=img_file.read())
    # Normalize the result to plain text.
    return result.get("text", "")
