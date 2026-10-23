from __future__ import annotations

from typing import List

from vision_client import get_google_vision_client
from vision_models import ImageTextRequest, normalize_detected_text


def detect_image_text(image_url: str, *, image_path: str | None = None) -> List[str]:
    """Detect text appearing inside an image using Google Cloud Vision OCR."""
    request = ImageTextRequest(image_url=image_url, image_path=image_path)
    client = get_google_vision_client()
    response = client.detect_text(request)
    return normalize_detected_text(response)
