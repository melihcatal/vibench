from __future__ import annotations

from typing import List, Dict

from google.cloud.vision_v1 import Image

from vision_client import build_google_vision_client, load_image_source
from vision_models import normalize_labels


GOOGLE_VISION_PROVIDER = "vision.googleapis.com"


def detect_image_labels(image_path: str, max_results: int = 10) -> List[Dict[str, float]]:
    source = load_image_source(image_path)
    client = build_google_vision_client()
    response = client.label_detection(image=Image(content=source.image_bytes), max_results=max_results)
    if response.error.message:
        raise RuntimeError(response.error.message)
    labels = [
        {"name": annotation.description, "score": annotation.score}
        for annotation in response.label_annotations
    ]
    return normalize_labels(labels)
