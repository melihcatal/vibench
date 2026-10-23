from __future__ import annotations

from vision_client import build_google_vision_image, get_google_vision_client
from vision_models import (
    ImageInput,
    ImageTextDetectionResult,
    normalize_google_vision_text,
)


def detect_image_text(image_input: ImageInput) -> ImageTextDetectionResult:
    client = get_google_vision_client()
    image = build_google_vision_image(image_input)
    response = client.text_detection(image=image)
    return normalize_google_vision_text(type(response).to_dict(response))
