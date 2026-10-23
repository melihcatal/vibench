from __future__ import annotations

from typing import Optional

from vision_client import get_google_vision_client, build_vision_image
from vision_models import ImageSource, LabelDetectionResult, normalize_label_annotations


def detect_image_labels(image_path: Optional[str] = None, image_url: Optional[str] = None, max_results: int = 15) -> LabelDetectionResult:
    client = get_google_vision_client()
    image = build_vision_image(ImageSource(image_path=image_path, image_url=image_url))
    response = client.label_detection(image=image, max_results=max_results)
    if response.error.message:
        raise RuntimeError(f"Google Cloud Vision API error: {response.error.message}")
    labels = normalize_label_annotations(response.label_annotations)
    return LabelDetectionResult(labels=labels, raw_response=getattr(response, "_pb", None))
