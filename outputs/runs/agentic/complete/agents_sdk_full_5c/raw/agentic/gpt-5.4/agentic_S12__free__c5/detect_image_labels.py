from __future__ import annotations

from typing import List

from google.cloud import vision

from vision_client import get_vision_client, load_image_content, load_image_uri
from vision_models import ImageLabel, normalize_confidence


GOOGLE_VISION_FEATURE = vision.Feature.Type.LABEL_DETECTION


def detect_image_labels(image_path: str | None = None, image_uri: str | None = None, max_results: int = 20) -> List[ImageLabel]:
    client = get_vision_client()
    image = load_image_uri(image_uri) if image_uri else load_image_content(image_path or "")
    response = client.label_detection(image=image, max_results=max_results)
    if response.error.message:
        raise RuntimeError(response.error.message)
    return [
        ImageLabel(name=label.description, confidence=normalize_confidence(label.score, 100.0))
        for label in response.label_annotations
    ]
