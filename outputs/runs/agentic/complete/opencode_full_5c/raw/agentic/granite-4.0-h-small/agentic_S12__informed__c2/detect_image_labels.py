# [SAME-SCENARIO] detect_image_labels.py

import os
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> dict:
    """Detects labels/objects in a static image using Azure AI Vision SDK.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: JSON response from the Azure AI Vision service containing detected labels.
    """
    client = VisionClient()
    return client.label_image(image_path)
