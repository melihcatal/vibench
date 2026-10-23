from __future__ import annotations

from typing import Optional

from vision_client import (
    build_image_source,
    get_google_vision_client,
    image_source_to_google_image,
)
from vision_models import ImageSafetyResult, SafetyCategory, safety_result_dict


LIKELIHOOD_SCORES = {
    "UNKNOWN": 0.0,
    "VERY_UNLIKELY": 0.05,
    "UNLIKELY": 0.2,
    "POSSIBLE": 0.5,
    "LIKELY": 0.8,
    "VERY_LIKELY": 0.95,
}


def score_image_safety(
    image_path: Optional[str] = None, image_uri: Optional[str] = None
) -> dict:
    image = build_image_source(image_path=image_path, image_uri=image_uri)
    client = get_google_vision_client()
    response = client.safe_search_detection(image=image_source_to_google_image(image))
    if response.error.message:
        raise RuntimeError(response.error.message)
    annotation = response.safe_search_annotation
    categories = [
        SafetyCategory(
            name="adult",
            likelihood=annotation.adult.name,
            score=LIKELIHOOD_SCORES.get(annotation.adult.name, 0.0),
        ),
        SafetyCategory(
            name="spoof",
            likelihood=annotation.spoof.name,
            score=LIKELIHOOD_SCORES.get(annotation.spoof.name, 0.0),
        ),
        SafetyCategory(
            name="medical",
            likelihood=annotation.medical.name,
            score=LIKELIHOOD_SCORES.get(annotation.medical.name, 0.0),
        ),
        SafetyCategory(
            name="violence",
            likelihood=annotation.violence.name,
            score=LIKELIHOOD_SCORES.get(annotation.violence.name, 0.0),
        ),
        SafetyCategory(
            name="racy",
            likelihood=annotation.racy.name,
            score=LIKELIHOOD_SCORES.get(annotation.racy.name, 0.0),
        ),
    ]
    sensitive = any(
        category.likelihood in {"POSSIBLE", "LIKELY", "VERY_LIKELY"}
        for category in categories
    )
    result = ImageSafetyResult(
        provider="google-cloud-vision", categories=categories, is_sensitive=sensitive
    )
    return safety_result_dict(result)
