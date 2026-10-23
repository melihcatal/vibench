import os
import json

from vision_client import VisionClient
from vision_models import normalize_labels

def detect_image_labels(image_path: str) -> dict:
    """Detect objects/labels in a static image using Amazon Rekognition.

    Returns a dict with normalized label information.
    """
    client = VisionClient(service='rekognition')
    # Rekognition expects bytes-like object
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.detect_labels(Image={'Bytes': image_bytes})
    # The SDK returns a list of labels with Confidence and Name
    raw_labels = response.get('Labels', [])
    return normalize_labels(raw_labels)
