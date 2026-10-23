from __future__ import annotations

from typing import Optional

from vision_client import build_vision_image, get_google_vision_client
from vision_models import ImageSource, SafetyScoreResult, normalize_safe_search


def score_image_safety(image_path: Optional[str] = None, image_url: Optional[str] = None, threshold: str = "LIKELY") -> SafetyScoreResult:
    client = get_google_vision_client()
    image = build_vision_image(ImageSource(image_path=image_path, image_url=image_url))
    response = client.safe_search_detection(image=image)
    if response.error.message:
        raise RuntimeError(f"Google Cloud Vision SafeSearch error: {response.error.message}")
    categories = normalize_safe_search(response.safe_search_annotation, threshold=threshold)
    return SafetyScoreResult(categories=categories, raw_response=getattr(response, "_pb", None))
