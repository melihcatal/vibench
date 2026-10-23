from __future__ import annotations

from typing import Dict, List

from vision_client import google_vision_annotate
from vision_models import ImageInput, normalize_labels


def detect_image_labels(
    image_path: str | None = None, image_url: str | None = None, max_results: int = 10
) -> List[Dict[str, float]]:
    image = ImageInput(image_path=image_path, image_url=image_url)
    result = google_vision_annotate(
        "LABEL_DETECTION", image=image, max_results=max_results
    )
    labels = normalize_labels(result.get("labelAnnotations", []))
    return [{"name": item.name, "score": item.score} for item in labels]
