from __future__ import annotations

from typing import Dict, List, Optional

from vision_client import build_vision_image, get_google_vision_client
from vision_models import normalize_vision_labels


PROVIDER = "google_cloud_vision"


def detect_image_labels(image_path: Optional[str] = None, image_uri: Optional[str] = None, max_results: int = 10) -> List[Dict[str, object]]:
    client = get_google_vision_client()
    image = build_vision_image(image_path=image_path, image_uri=image_uri)
    response = client.label_detection(image=image, max_results=max_results)
    labels = []
    for label in response.label_annotations:
        labels.append(
            {
                "name": label.description,
                "confidence": float(label.score),
                "categories": [],
            }
        )
    return normalize_vision_labels(labels)
