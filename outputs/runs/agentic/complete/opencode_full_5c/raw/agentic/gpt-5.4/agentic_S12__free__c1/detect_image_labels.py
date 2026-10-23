from __future__ import annotations

from vision_client import (
    build_google_vision_image,
    get_google_vision_client,
    load_image_input,
)
from vision_models import LabelDetectionResult, normalize_labels


def detect_image_labels(
    image_path: str | None = None, image_uri: str | None = None
) -> dict:
    image_input = load_image_input(image_path=image_path, image_uri=image_uri)
    client = get_google_vision_client()
    response = client.label_detection(image=build_google_vision_image(image_input))
    labels = [
        {"name": annotation.description, "score": annotation.score}
        for annotation in response.label_annotations
    ]
    return LabelDetectionResult(
        provider="google-cloud-vision", labels=normalize_labels(labels)
    ).to_dict()
