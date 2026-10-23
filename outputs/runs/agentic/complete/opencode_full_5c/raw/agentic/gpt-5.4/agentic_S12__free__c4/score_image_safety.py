from __future__ import annotations

from vision_client import (
    get_google_vision_client,
    load_image_input,
    to_google_vision_image,
)
from vision_models import ImageSafetyResult, normalize_google_safe_search


def score_image_safety(
    image_path: str, mime_type: str = "image/jpeg"
) -> ImageSafetyResult:
    client = get_google_vision_client()
    image = to_google_vision_image(load_image_input(image_path, mime_type=mime_type))
    response = client.safe_search_detection(image=image)
    return normalize_google_safe_search(response)
