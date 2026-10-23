# [SAME-SCENARIO] extract_text.py
"""Extract plain text from a scanned document image using a third‑party OCR provider."""

from document_client import OCRClient
from document_models import OCRResponse


def extract_text(image_path: str) -> str:
    """Extract plain text from the given image file.

    Args:
        image_path: Path to a local scanned image file.

    Returns:
        The plain text extracted from the document.
    """
    client = OCRClient()  # concrete provider (e.g., AWS Textract, Google Vision)
    response: OCRResponse = client.extract_text(image_path)
    return response.text
