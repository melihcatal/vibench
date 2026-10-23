from __future__ import annotations

from vision_client import AzureVisionClient
from vision_models import VisionRequest


def score_image_safety(image_path: str, language: str | None = None):
    client = AzureVisionClient()
    return client.score_safety(VisionRequest(image_path=image_path, language=language))
