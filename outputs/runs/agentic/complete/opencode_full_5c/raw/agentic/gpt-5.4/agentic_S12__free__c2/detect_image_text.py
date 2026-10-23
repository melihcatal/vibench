from __future__ import annotations

from typing import Dict, List

from vision_client import google_vision_annotate
from vision_models import ImageInput, normalize_texts


def detect_image_text(
    image_path: str | None = None, image_url: str | None = None
) -> List[Dict[str, float]]:
    image = ImageInput(image_path=image_path, image_url=image_url)
    result = google_vision_annotate("TEXT_DETECTION", image=image, max_results=50)
    annotations = result.get("textAnnotations", [])
    items = [
        {"text": entry.get("description", ""), "score": entry.get("confidence", 0.0)}
        for entry in annotations[1:]
    ]
    texts = normalize_texts(items)
    return [{"text": item.text, "score": item.score} for item in texts]
