from __future__ import annotations

from vision_client import (
    get_google_vision_client,
    load_image_input,
    to_google_vision_image,
)
from vision_models import ImageTextResult, normalize_google_vision_text


def detect_image_text(
    image_path: str, mime_type: str = "image/jpeg"
) -> ImageTextResult:
    client = get_google_vision_client()
    image = to_google_vision_image(load_image_input(image_path, mime_type=mime_type))
    response = client.text_detection(image=image)
    return normalize_google_vision_text(response)
