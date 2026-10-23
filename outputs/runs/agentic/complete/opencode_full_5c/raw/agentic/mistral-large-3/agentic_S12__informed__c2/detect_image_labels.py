import os
from typing import List
from vision_client import GoogleVisionClient
from vision_models import normalize_labels


def detect_image_labels(image_path: str) -> List[dict]:
    """
    Detects labels or objects in a static image using Google Cloud Vision.
    """
    client = GoogleVisionClient()
    labels = client.detect_labels(image_path)
    return normalize_labels(labels)
