from __future__ import annotations

from vision_client import AzureVisionClient
from vision_models import VisionRequest


def detect_image_text(image_path: str, language: str | None = None):
    client = AzureVisionClient()
    return client.detect_text(VisionRequest(image_path=image_path, language=language))
