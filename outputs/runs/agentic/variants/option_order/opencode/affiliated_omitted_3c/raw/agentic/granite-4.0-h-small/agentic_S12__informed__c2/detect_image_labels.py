import os
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> list:
    """Detect labels/objects in a static image using Azure AI Vision.
    Returns a list of detected label strings.
    """
    client = VisionClient()
    # Azure AI Vision SDK client initialized in vision_client
    labels = client.label_image(image_path)
    # Normalize output to simple list of label names
    return [label.name for label in labels]
