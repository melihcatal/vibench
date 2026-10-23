import os
from typing import List
from vision_client import GoogleVisionClient
from vision_models import normalize_text_detections


def detect_image_text(image_path: str) -> List[dict]:
    """
    Detects text appearing inside an image using Google Cloud Vision.
    """
    client = GoogleVisionClient()
    texts = client.detect_text(image_path)
    return normalize_text_detections(texts)
