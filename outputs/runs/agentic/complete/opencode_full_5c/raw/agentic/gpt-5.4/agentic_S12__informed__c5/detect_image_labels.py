from __future__ import annotations

from vision_client import (
    build_google_vision_image,
    get_google_vision_client,
    load_image_source,
)
from vision_models import LabelDetectionResult, normalize_labels


def detect_image_labels(
    image_path: str | None = None,
    image_uri: str | None = None,
    image_bytes: bytes | None = None,
    max_results: int = 20,
) -> dict:
    client = get_google_vision_client()
    source = load_image_source(
        image_path=image_path, image_uri=image_uri, image_bytes=image_bytes
    )
    image = build_google_vision_image(source)
    response = client.label_detection(image=image, max_results=max_results)
    labels = normalize_labels(
        [
            {"name": annotation.description, "confidence": annotation.score * 100.0}
            for annotation in response.label_annotations
        ]
    )
    return LabelDetectionResult(labels=labels).to_dict()
