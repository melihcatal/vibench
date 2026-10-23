from __future__ import annotations

from google.cloud import vision

from vision_client import build_client, make_image
from vision_models import normalize_text


def detect_image_text(image_path: str):
    client = build_client()
    image = make_image(image_path)
    response = client.text_detection(image=image)
    return [normalize_text(item) for item in response.text_annotations]
