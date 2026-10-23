from __future__ import annotations

from typing import Optional

from google.cloud import vision

from vision_client import DEFAULT_PROVIDER, get_vision_client, make_vision_image
from vision_models import DetectionResult, SafetyCategory, summarize_safety


SAFE_SEARCH_FIELDS = {
    "adult": vision.Likelihood,
    "spoof": vision.Likelihood,
    "medical": vision.Likelihood,
    "violence": vision.Likelihood,
    "racy": vision.Likelihood,
}


def _likelihood_to_score(value: int) -> float:
    return min(max(value / 5.0, 0.0), 1.0)


def score_image_safety(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> dict:
    client = get_vision_client()
    image = make_vision_image(image_path=image_path, image_bytes=image_bytes)
    response = client.safe_search_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)

    annotation = response.safe_search_annotation
    categories = [
        SafetyCategory(name=field, confidence=_likelihood_to_score(int(getattr(annotation, field))))
        for field in SAFE_SEARCH_FIELDS
    ]
    result = DetectionResult(
        provider=DEFAULT_PROVIDER,
        image_uri=image_path,
        safety_categories=categories,
        raw={
            field: vision.Likelihood(getattr(annotation, field)).name
            for field in SAFE_SEARCH_FIELDS
        },
    )
    payload = result.to_dict()
    payload["summary"] = summarize_safety(categories, threshold=0.6)
    return payload
