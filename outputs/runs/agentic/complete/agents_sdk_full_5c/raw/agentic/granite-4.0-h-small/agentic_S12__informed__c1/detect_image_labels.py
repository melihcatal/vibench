import os
from vision_client import VisionClient

def detect_image_labels(image_path: str) -> dict:
    """Detect objects/labels in a static image using Alibaba Cloud Vision API.
    Returns a dict with label annotations.
    """
    with open(image_path, "rb") as img_file:
        result = VisionClient().vision_client.detect_objects(image=img_file.read())
    # Normalize result to a simple list of label strings
    labels = [label['name'] for label in result.get('objects', [])]
    return {'labels': labels}