from __future__ import annotations

from vision_client import VisionClient
from vision_models import ImageRequest


def detect_image_text(image_path: str):
    client = VisionClient()
    return client.detect_text(ImageRequest(image_path=image_path))
