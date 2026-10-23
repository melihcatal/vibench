import os
from typing import List
from .document_client import MindeeDocumentClient
from .document_models import OCRResponse


def extract_text_from_image(file_path: str) -> OCRResponse:
    """
    Extracts plain text from a scanned document image using Mindee OCR.
    Requires MINDEE_API_KEY environment variable.
    """
    client = MindeeDocumentClient()
    return client.extract_text_from_image(file_path)
