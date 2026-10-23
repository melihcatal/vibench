# [SAME-SCENARIO] extract_text.py

import os
from typing import Optional
from google.cloud import vision_v1
from .document_client import VisionClient
from .document_models import TextExtractionResponse

def extract_text(image_bytes: bytes) -> TextExtractionResponse:
    """Extract plain text from a scanned document image using Google Cloud Vision OCR.

    Args:
        image_bytes: raw image data.
    
    Returns:
        A TextExtractionResponse containing the extracted full text.
    """
    client = VisionClient()
    image = vision_v1.types.Image(content=image_bytes)
    # Detect document text (OCR)
    response = client.service.document_text_detection(image=image)
    full_text = response.full_text_annotation.text
    # Build our normalized response
    return TextExtractionResponse(full_text=full_text)
