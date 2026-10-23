from __future__ import annotations

from vision_client import (
    get_google_vision_client,
    load_image_input,
    to_google_vision_image,
)
from vision_models import LabelDetectionResult, normalize_google_vision_labels


def detect_image_labels(
    image_path: str, mime_type: str = "image/jpeg"
) -> LabelDetectionResult:
    client = get_google_vision_client()
    image = to_google_vision_image(load_image_input(image_path, mime_type=mime_type))
    response = client.annotate_image(
        {
            "image": image,
            "features": [
                {"type_": "LABEL_DETECTION", "max_results": 10},
                {"type_": "OBJECT_LOCALIZATION", "max_results": 10},
            ],
        }
    )
    return normalize_google_vision_labels(response)
