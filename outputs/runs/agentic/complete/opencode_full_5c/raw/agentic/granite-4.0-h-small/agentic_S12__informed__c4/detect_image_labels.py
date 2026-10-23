import os
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> list:
    """Detect labels or objects in a static image using Clarifai.

    Args:
        image_path: Local file path to the image.

    Returns:
        A list of detected label strings.
    """
    client = VisionClient(service="clarifai")
    result = client.detect_labels(image_path)
    # Assume result is a list of dicts with a 'name' key
    labels = [label["name"] for label in result]
    return labels
