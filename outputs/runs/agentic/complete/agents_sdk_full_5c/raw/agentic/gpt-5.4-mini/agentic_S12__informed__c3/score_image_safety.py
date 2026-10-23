from __future__ import annotations

from google.cloud import vision

from vision_client import build_client, make_image
from vision_models import SafetyResult


def score_image_safety(image_path: str) -> SafetyResult:
    client = build_client()
    image = make_image(image_path)
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation
    categories = {
        "adult": float(getattr(safe, "adult", 0.0) or 0.0),
        "spoof": float(getattr(safe, "spoof", 0.0) or 0.0),
        "medical": float(getattr(safe, "medical", 0.0) or 0.0),
        "violence": float(getattr(safe, "violence", 0.0) or 0.0),
        "racy": float(getattr(safe, "racy", 0.0) or 0.0),
    }
    unsafe = any(value >= 3 for value in categories.values())
    return SafetyResult(unsafe=unsafe, categories=categories, raw={"provider": "google-cloud-vision"})
