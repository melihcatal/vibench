from __future__ import annotations

from vision_client import analyze_image
from vision_models import VisionRequest


def detect_image_labels(image_path: str, max_results: int = 10):
    request = VisionRequest(image_path=image_path, max_results=max_results)
    response = analyze_image(request, features=["OBJECTS"])
    return [finding.name for finding in response.findings[:max_results]]
