import os
from .document_client import OcrClient
from .document_models import TextResult

def extract_text(image_path: str) -> TextResult:
    """Extract plain text from a scanned document image using Google Vision OCR.
    """
    client = OcrClient()
    response = client.annotate_image(image_path)
    # Normalize response to our TextResult model
    return TextResult(text=response["full_text"], blocks=response.get("blocks"))
