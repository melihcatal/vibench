from __future__ import annotations

from typing import Optional

from vision_client import (
    GOOGLE_VISION_PROVIDER,
    build_google_vision_image,
    get_google_vision_client,
)
from vision_models import LabelDetectionResult, normalize_label_annotations


def detect_image_labels(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    max_results: int = 10,
) -> dict:
    client = get_google_vision_client()
    image = build_google_vision_image(image_path=image_path, image_uri=image_uri)
    response = client.label_detection(image=image, max_results=max_results)
    if response.error.message:
        raise RuntimeError(response.error.message)
    result = LabelDetectionResult(
        provider=GOOGLE_VISION_PROVIDER,
        labels=normalize_label_annotations(response.label_annotations),
        raw_response={"label_count": len(response.label_annotations)},
    )
    return result.to_dict()
