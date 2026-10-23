from __future__ import annotations

from vision_client import analyze_image
from vision_models import VisionRequest


def describe_image(image_path: str, language: str = "en"):
    request = VisionRequest(image_path=image_path, language=language)
    response = analyze_image(request, features=["CAPTION"])
    return response.summary or ""
