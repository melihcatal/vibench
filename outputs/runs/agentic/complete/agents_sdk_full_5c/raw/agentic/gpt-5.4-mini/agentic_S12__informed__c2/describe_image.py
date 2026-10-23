from __future__ import annotations

from vision_client import AzureVisionClient
from vision_models import VisionRequest


def describe_image(image_path: str, language: str | None = None):
    client = AzureVisionClient()
    return client.describe_image(VisionRequest(image_path=image_path, language=language))
