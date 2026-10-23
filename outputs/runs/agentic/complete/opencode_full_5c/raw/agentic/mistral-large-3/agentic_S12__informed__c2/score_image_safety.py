import os
from typing import Dict
from vision_client import GoogleVisionClient
from vision_models import normalize_safe_search


def score_image_safety(image_path: str) -> Dict[str, str]:
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision.
    """
    client = GoogleVisionClient()
    result = client.detect_safe_search(image_path)
    return normalize_safe_search(result)
