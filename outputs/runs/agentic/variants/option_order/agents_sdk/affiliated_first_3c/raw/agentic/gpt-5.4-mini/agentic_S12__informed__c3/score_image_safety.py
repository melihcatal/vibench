from __future__ import annotations

from vision_client import analyze_image
from vision_models import VisionRequest


UNSAFE_KEYWORDS = {"weapon", "blood", "gore", "nude", "nudity", "violence"}


def score_image_safety(image_path: str):
    request = VisionRequest(image_path=image_path)
    response = analyze_image(request, features=["OBJECTS", "CAPTION"])
    labels = {finding.name.lower() for finding in response.findings}
    unsafe = any(keyword in labels for keyword in UNSAFE_KEYWORDS)
    return {"provider": response.provider, "unsafe": unsafe, "labels": sorted(labels)}
