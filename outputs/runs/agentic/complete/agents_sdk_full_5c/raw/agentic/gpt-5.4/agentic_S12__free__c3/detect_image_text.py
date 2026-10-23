from __future__ import annotations

from typing import Optional

from vision_client import build_vision_image, get_google_vision_client
from vision_models import ImageSource, normalize_text_annotations


def detect_image_text(image_path: Optional[str] = None, image_url: Optional[str] = None):
    client = get_google_vision_client()
    image = build_vision_image(ImageSource(image_path=image_path, image_url=image_url))
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise RuntimeError(f"Google Cloud Vision OCR error: {response.error.message}")
    return normalize_text_annotations(response)
