import os
from vision_client import VisionClient

def detect_image_text(image_path: str) -> dict:
    """Detect embedded text in an image using Alibaba Cloud Vision API.
    Returns a dict with detected text lines.
    """
    with open(image_path, "rb") as img_file:
        result = VisionClient().vision_client.detect_text(image=img_file.read())
    # Normalize to list of text strings
    lines = [line['content'] for line in result.get('text', [])]
    return {'detected_text': lines}
