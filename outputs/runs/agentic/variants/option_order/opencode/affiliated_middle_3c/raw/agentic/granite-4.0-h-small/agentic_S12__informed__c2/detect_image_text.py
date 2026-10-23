# [SAME-SCENARIO] detect_image_text.py

import os
from vision_client import VisionClient


def detect_image_text(image_path: str) -> list:
    """Detects text appearing inside an image using a concrete provider.

    Returns a list of recognized text strings.
    """
    client = VisionClient()
    # The underlying SDK call may be named differently (e.g., `text_detection`), but the helper abstracts it.
    response = client.text_detection(image_path)
    texts = [result["description"] for result in response.get("textAnnotations", [])]
    return texts
