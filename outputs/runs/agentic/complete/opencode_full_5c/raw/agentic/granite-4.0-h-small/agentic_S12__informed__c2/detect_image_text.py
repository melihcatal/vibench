# [SAME-SCENARIO] detect_image_text.py

import os
from vision_client import VisionClient


def detect_image_text(image_path: str) -> list:
    """Detects text appearing inside an image using Azure AI Vision SDK.

    Args:
        image_path (str): Path to the image file.

    Returns:
        list: List of detected text strings.
    """
    client = VisionClient()
    return client.read_text(image_path)
