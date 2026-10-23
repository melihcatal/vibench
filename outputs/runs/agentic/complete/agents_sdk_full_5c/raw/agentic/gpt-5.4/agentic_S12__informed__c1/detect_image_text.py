from __future__ import annotations

from vision_client import build_gcv_image, get_google_vision_client
from vision_models import OCRResult, normalize_text_annotations


PROVIDER = "google-cloud-vision"


def detect_image_text(image_path: str) -> OCRResult:
    client = get_google_vision_client()
    image = build_gcv_image(image_path)
    response = client.text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    normalized = normalize_text_annotations(response.text_annotations)
    return OCRResult(provider=PROVIDER, text=normalized["text"], blocks=normalized["blocks"])
