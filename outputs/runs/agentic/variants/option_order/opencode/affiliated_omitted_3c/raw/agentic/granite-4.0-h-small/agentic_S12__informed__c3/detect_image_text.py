# detect_image_text.py
import os
from google.cloud import vision


def detect_image_text(image_path):
    """Detect OCR text appearing inside an image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return [text.description.strip() for text in texts]
