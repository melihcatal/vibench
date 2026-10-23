from __future__ import annotations

from typing import List

from google.cloud import vision

from vision_client import get_vision_client, load_image_content, load_image_uri
from vision_models import SafetyCategory


LIKELIHOOD_SCORE = {
    vision.Likelihood.UNKNOWN: 0.0,
    vision.Likelihood.VERY_UNLIKELY: 0.05,
    vision.Likelihood.UNLIKELY: 0.2,
    vision.Likelihood.POSSIBLE: 0.5,
    vision.Likelihood.LIKELY: 0.8,
    vision.Likelihood.VERY_LIKELY: 0.98,
}


def score_image_safety(image_path: str | None = None, image_uri: str | None = None) -> List[SafetyCategory]:
    client = get_vision_client()
    image = load_image_uri(image_uri) if image_uri else load_image_content(image_path or "")
    response = client.safe_search_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    annotation = response.safe_search_annotation
    return [
        SafetyCategory("adult", round(LIKELIHOOD_SCORE[annotation.adult] * 100.0, 2)),
        SafetyCategory("spoof", round(LIKELIHOOD_SCORE[annotation.spoof] * 100.0, 2)),
        SafetyCategory("medical", round(LIKELIHOOD_SCORE[annotation.medical] * 100.0, 2)),
        SafetyCategory("violence", round(LIKELIHOOD_SCORE[annotation.violence] * 100.0, 2)),
        SafetyCategory("racy", round(LIKELIHOOD_SCORE[annotation.racy] * 100.0, 2)),
    ]
