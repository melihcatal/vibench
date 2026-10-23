from __future__ import annotations

from vision_client import build_gcv_image, get_google_vision_client
from vision_models import LabelDetectionResult, normalize_label_annotations


PROVIDER = "google-cloud-vision"


def detect_image_labels(image_path: str, max_results: int = 10) -> LabelDetectionResult:
    client = get_google_vision_client()
    image = build_gcv_image(image_path)
    response = client.label_detection(image=image, max_results=max_results)
    if response.error.message:
        raise RuntimeError(response.error.message)
    labels = normalize_label_annotations(response.label_annotations)
    return LabelDetectionResult(provider=PROVIDER, labels=labels)
