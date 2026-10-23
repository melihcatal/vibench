from __future__ import annotations

from typing import List

from google.cloud import vision

from vision_client import build_vision_image, get_google_vision_client
from vision_models import LabelDetectionResult


GOOGLE_VISION_FEATURE = vision.Feature.Type.LABEL_DETECTION


def detect_image_labels(image_path: str, max_results: int = 10) -> List[LabelDetectionResult]:
    client = get_google_vision_client()
    image = build_vision_image(image_path)
    response = client.label_detection(image=image, max_results=max_results)
    if response.error.message:
        raise RuntimeError(response.error.message)
    results: List[LabelDetectionResult] = []
    for label in response.label_annotations:
        results.append(
            LabelDetectionResult(
                name=label.description,
                confidence=float(label.score),
                parents=[],
            )
        )
    return results
