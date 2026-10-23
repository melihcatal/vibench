from __future__ import annotations

from vision_client import VisionClient
from vision_models import ImageRequest


def score_image_safety(image_path: str):
    client = VisionClient()
    return client.score_safety(ImageRequest(image_path=image_path))
