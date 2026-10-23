# score_image_safety.py
import os
from google.cloud import vision


def score_image_safety(image_path):
    """Check an image for unsafe or policy-sensitive visual content using Google Cloud Vision SafeSearch."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    safe = client.safe_search_detection(image=image)
    categories = {
        "adult": safe.safe_search_annotation.adult,
        "spoof": safe.safe_search_annotation.spoof,
        "medical": safe.safe_search_annotation.medical,
        "violence": safe.safe_search_annotation.violence,
        "racy": safe.safe_search_annotation.racy,
    }
    return categories
