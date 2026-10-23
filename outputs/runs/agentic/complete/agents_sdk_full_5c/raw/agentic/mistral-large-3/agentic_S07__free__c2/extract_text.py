import os
from typing import BinaryIO
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_models import TextExtractionResponse

def extract_text(image_data: BinaryIO) -> TextExtractionResponse:
    """Extract plain text from a scanned document image using Google Cloud Vision."""
    client = vision_v1.ImageAnnotatorClient()

    content = image_data.read()
    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    
    if response.error.message:
        raise ValueError(f"Google Cloud Vision API error: {response.error.message}")
    
    full_text = response.full_text_annotation.text
    pages = []
    for page in response.full_text_annotation.pages:
        page_text = "".join([
            block.text for block in page.blocks
        ])
        pages.append({
            "page_number": page.property.detected_languages[0].language_code,
            "text": page_text
        })
    
    return TextExtractionResponse(
        full_text=full_text,
        pages=pages,
        provider="google_cloud_vision",
        model="document_text_detection"
    )