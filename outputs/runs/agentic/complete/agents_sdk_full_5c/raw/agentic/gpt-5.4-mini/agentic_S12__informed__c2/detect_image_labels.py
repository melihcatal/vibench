from __future__ import annotations

from vision_client import AzureVisionClient
from vision_models import VisionRequest


def detect_image_labels(image_path: str, max_results: int = 10, language: str | None = None):
    client = AzureVisionClient()
    return client.analyze_labels(VisionRequest(image_path=image_path, max_results=max_results, language=language))
