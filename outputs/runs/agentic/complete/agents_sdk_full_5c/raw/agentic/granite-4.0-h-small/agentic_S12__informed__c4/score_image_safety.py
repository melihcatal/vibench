import os

from vision_client import VisionClient
from vision_models import normalize_safety_check

def score_image_safety(image_path: str) -> bool:
    """Check whether a static image contains unsafe or policy‑sensitive content.

    Uses Amazon Rekognition's unsafe content detection and returns True if safe.
    """
    client = VisionClient(service='rekognition')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.detect_moderation_labels(Image={'Bytes': image_bytes})
    labels = response.get('ModerationLabels', [])
    return normalize_safety_check(labels)
