from __future__ import annotations

from vision_client import get_client, make_image
from vision_models import ImageRequest, SafetyResult


def score_image_safety(image_path: str):
    request = ImageRequest(image_path=image_path)
    client = get_client()
    image = make_image(request.image_path)
    response = client.safe_search_detection(image=image)
    annotation = response.safe_search_annotation
    categories = {
        "adult": float(annotation.adult),
        "violence": float(annotation.violence),
        "racy": float(annotation.racy),
        "medical": float(annotation.medical),
        "spoof": float(annotation.spoof),
    }
    safe = all(v <= 2.0 for v in categories.values())
    reason = "SafeSearch levels are within a low-risk range."
    return SafetyResult(safe=safe, categories=categories, reason=reason)
