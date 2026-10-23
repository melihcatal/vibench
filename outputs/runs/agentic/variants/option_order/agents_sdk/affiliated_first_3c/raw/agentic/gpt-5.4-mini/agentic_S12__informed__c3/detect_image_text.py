from __future__ import annotations

from vision_client import analyze_image
from vision_models import VisionRequest


def detect_image_text(image_path: str):
    request = VisionRequest(image_path=image_path)
    response = analyze_image(request, features=["READ"])
    return [finding.text for finding in response.findings if finding.text]
