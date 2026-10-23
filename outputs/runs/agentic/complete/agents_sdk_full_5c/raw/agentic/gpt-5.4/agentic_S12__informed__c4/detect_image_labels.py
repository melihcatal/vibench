from __future__ import annotations

from typing import Optional

from vision_client import DEFAULT_MODEL, DEFAULT_PROVIDER, build_image_source, load_vision_client
from vision_models import LabelDetection, VisionResult, normalize_confidence


def detect_image_labels(path: Optional[str] = None, uri: Optional[str] = None, max_results: int = 10) -> dict:
    client = load_vision_client()
    image, image_meta = build_image_source(path=path, uri=uri)
    response = client.label_detection(image=image, max_results=max_results)
    labels = [
        LabelDetection(
            name=annotation.description,
            confidence=normalize_confidence(annotation.score),
            categories=list(annotation.topicality and [] or []),
        )
        for annotation in response.label_annotations
    ]
    result = VisionResult(
        provider=DEFAULT_PROVIDER,
        model=DEFAULT_MODEL,
        image=image_meta,
        labels=labels,
        raw_response={"error": response.error.message} if response.error.message else {},
    )
    return result.to_dict()
