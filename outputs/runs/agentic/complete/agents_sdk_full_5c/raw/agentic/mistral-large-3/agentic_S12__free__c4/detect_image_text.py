import os
from typing import List
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import TextDetectionResponse


def detect_text(image_path: str) -> TextDetectionResponse:
    """Detect text in a static image using Google Cloud Vision API."""
    client = get_vision_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision_v1.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    return TextDetectionResponse(
        full_text=texts[0].description if texts else "",
        text_annotations=[text.description for text in texts[1:]]
    )