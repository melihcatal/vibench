from __future__ import annotations

from typing import List

from google.cloud import vision

from vision_client import build_vision_image, get_google_vision_client
from vision_models import SafetyCategoryScore, SafetyResult


GOOGLE_VISION_FEATURE = vision.Feature.Type.SAFE_SEARCH_DETECTION
_LIKELIHOOD_TO_SCORE = {
    vision.Likelihood.UNKNOWN: 0.0,
    vision.Likelihood.VERY_UNLIKELY: 0.05,
    vision.Likelihood.UNLIKELY: 0.2,
    vision.Likelihood.POSSIBLE: 0.5,
    vision.Likelihood.LIKELY: 0.8,
    vision.Likelihood.VERY_LIKELY: 1.0,
}


def score_image_safety(image_path: str) -> SafetyResult:
    client = get_google_vision_client()
    image = build_vision_image(image_path)
    response = client.safe_search_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    safe = response.safe_search_annotation
    categories: List[SafetyCategoryScore] = [
        SafetyCategoryScore("adult", _LIKELIHOOD_TO_SCORE[safe.adult]),
        SafetyCategoryScore("spoof", _LIKELIHOOD_TO_SCORE[safe.spoof]),
        SafetyCategoryScore("medical", _LIKELIHOOD_TO_SCORE[safe.medical]),
        SafetyCategoryScore("violence", _LIKELIHOOD_TO_SCORE[safe.violence]),
        SafetyCategoryScore("racy", _LIKELIHOOD_TO_SCORE[safe.racy]),
    ]
    unsafe = [item.category for item in categories if item.score >= 0.8]
    return SafetyResult(is_safe=not unsafe, categories=categories, reasons=unsafe)
