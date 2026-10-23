from __future__ import annotations

from typing import Optional

from google.cloud import vision

from vision_client import DEFAULT_PROVIDER, get_vision_client, make_vision_image
from vision_models import DetectionResult, ImageLabel


FEATURE_MAX_RESULTS = 20


def detect_image_labels(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> dict:
    client = get_vision_client()
    image = make_vision_image(image_path=image_path, image_bytes=image_bytes)
    response = client.label_detection(image=image, max_results=FEATURE_MAX_RESULTS)
    if response.error.message:
        raise RuntimeError(response.error.message)

    labels = [
        ImageLabel(name=annotation.description, confidence=float(annotation.score))
        for annotation in response.label_annotations
    ]
    result = DetectionResult(
        provider=DEFAULT_PROVIDER,
        image_uri=image_path,
        labels=labels,
        raw={
            "label_annotations": [
                {"description": item.description, "score": float(item.score)}
                for item in response.label_annotations
            ]
        },
    )
    return result.to_dict()
