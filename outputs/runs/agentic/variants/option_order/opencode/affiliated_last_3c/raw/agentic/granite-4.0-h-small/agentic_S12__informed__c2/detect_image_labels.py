# detect_image_labels.py
import json
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> list:
    """Detect labels/objects in a static image using a concrete provider and return the results.

    Uses Azure AI Vision SDK for demonstration.
    """
    client = VisionClient()
    result = client.label_image(image_path)
    # Normalize response to a simple list of label strings
    labels = [item["name"] for item in result.get("labels", [])]
    return labels
