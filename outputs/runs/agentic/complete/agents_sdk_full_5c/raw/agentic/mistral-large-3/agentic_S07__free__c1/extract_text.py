import os
from typing import BinaryIO
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_models import OCRTextResponse

def extract_text(image_data: BinaryIO) -> OCRTextResponse:
    """Extract plain text from a scanned document image using Google Cloud Vision."""
    client = vision_v1.ImageAnnotatorClient()
    content = image_data.read()
    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    
    if response.error.message:
        raise ValueError(f"Google Cloud Vision API error: {response.error.message}")
    
    full_text = response.full_text_annotation.text
    return OCRTextResponse(text=full_text, language=response.full_text_annotation.language)