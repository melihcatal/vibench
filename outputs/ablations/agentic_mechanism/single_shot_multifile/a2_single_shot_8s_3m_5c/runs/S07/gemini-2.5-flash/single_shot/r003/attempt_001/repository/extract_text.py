import os
from typing import Optional

from google.cloud import vision_v1

from document_client import get_gcp_vision_client
from document_models import DocumentInput, TextExtractionOutput

def extract_plain_text(
    document_input: DocumentInput,
) -> TextExtractionOutput:
    """Extracts plain text from a document image using Google Cloud Vision API."""
    client = get_gcp_vision_client()

    image = vision_v1.Image(content=document_input.image_bytes)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    full_text = texts[0].description if texts else ""

    return TextExtractionOutput(text=full_text)
