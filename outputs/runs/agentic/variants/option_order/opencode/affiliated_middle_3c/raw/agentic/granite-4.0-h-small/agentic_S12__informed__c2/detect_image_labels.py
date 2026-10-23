# [SAME-SCENARIO] detect_image_labels.py

import os
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> list:
    """Detects labels/objects in a static image using a concrete provider.

    Returns a list of detected label strings.
    """
    client = VisionClient()
    # The client uses environment variables to select the provider (e.g., GOOGLE_APPLICATION_CREDENTIALS for Google Cloud Vision).
    response = client.label_detection(image_path)
    # Normalize response to a simple list of label names.
    labels = [
        entry["description"]
        for entry in response["labelAnnotations"]
        if "description" in entry
    ]
    return labels
