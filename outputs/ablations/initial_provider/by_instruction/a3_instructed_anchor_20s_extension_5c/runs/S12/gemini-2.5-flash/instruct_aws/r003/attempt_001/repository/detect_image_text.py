import os
from google.cloud import vision

def detect_image_text(image_bytes: bytes) -> dict:
    """
    Detects text appearing inside an image using Google Cloud Vision API.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return {"text_annotations": [{"description": text.description, "bounding_poly": text.bounding_poly} for text in texts]}
