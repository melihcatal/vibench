from __future__ import annotations

from vision_client import build_google_vision_image, get_google_vision_client
from vision_models import (
    ImageInput,
    LabelDetectionResult,
    normalize_google_vision_labels,
)


def detect_image_labels(image_input: ImageInput) -> LabelDetectionResult:
    client = get_google_vision_client()
    image = build_google_vision_image(image_input)
    response = client.annotate_image(
        {
            "image": image,
            "features": [
                {"type_": "LABEL_DETECTION", "max_results": 20},
                {"type_": "OBJECT_LOCALIZATION", "max_results": 20},
            ],
        }
    )
    return normalize_google_vision_labels(type(response).to_dict(response))
