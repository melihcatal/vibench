from __future__ import annotations

from vision_client import VisionClient
from vision_models import ImageRequest


def detect_image_labels(image_path: str, max_labels: int = 10):
    client = VisionClient()
    return client.detect_labels(ImageRequest(image_path=image_path, max_labels=max_labels))
