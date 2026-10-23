from __future__ import annotations

from vision_client import (
    build_google_vision_image,
    get_google_vision_client,
    load_image_input,
)
from vision_models import ImageTextDetectionResult


def detect_image_text(
    image_path: str | None = None, image_uri: str | None = None
) -> dict:
    image_input = load_image_input(image_path=image_path, image_uri=image_uri)
    client = get_google_vision_client()
    response = client.text_detection(image=build_google_vision_image(image_input))
    annotations = response.text_annotations
    full_text = annotations[0].description if annotations else ""
    lines = [line for line in full_text.splitlines() if line.strip()]
    return ImageTextDetectionResult(
        provider="google-cloud-vision", text=full_text, lines=lines
    ).to_dict()
