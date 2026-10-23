import os
from vision_client import VisionClient


def detect_image_text(image_path: str) -> list:
    """Detect any text appearing inside an image (OCR) using Azure AI Vision.
    Returns a list of detected text strings.
    """
    client = VisionClient()
    text_blocks = client.ocr_image(image_path)
    # Return plain strings, flatten if necessary
    return [block.text for line in text_blocks for block in line.words]
