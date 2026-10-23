import os
from vision_client import VisionClient


def detect_image_text(image_path: str) -> list:
    """Detect text appearing inside an image using Google Cloud Vision.

    Args:
        image_path: Local file path to the image.

    Returns:
        A list of detected text strings.
    """
    client = VisionClient(service="google_vision")
    result = client.detect_text(image_path)
    # Assume result is a list of dicts with a 'description' key
    texts = [text["description"] for text in result]
    return texts
