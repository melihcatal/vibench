from __future__ import annotations

from pathlib import Path
from typing import List

from vision_client import get_google_vision_client, read_image_bytes
from vision_models import OCRResult, normalize_text_items


def detect_image_text(image_path: str | Path) -> OCRResult:
    """Detect text appearing inside an image using Google Cloud Vision API."""
    client = get_google_vision_client()
    image_bytes = read_image_bytes(image_path)
    response = client.text_detection(image={"content": image_bytes})
    annotations = getattr(response, "text_annotations", []) or []
    texts: List[str] = [getattr(a, "description", "") for a in annotations if getattr(a, "description", None)]
    normalized = normalize_text_items(texts)
    return OCRResult(text=normalized[0] if normalized else "", words=normalized[1:] if len(normalized) > 1 else [], raw=response)
