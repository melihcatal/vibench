from __future__ import annotations

from typing import Dict, List

from vision_client import google_vision_annotate
from vision_models import ImageInput, normalize_safety


def score_image_safety(
    image_path: str | None = None, image_url: str | None = None
) -> List[Dict[str, object]]:
    image = ImageInput(image_path=image_path, image_url=image_url)
    result = google_vision_annotate("SAFE_SEARCH_DETECTION", image=image, max_results=1)
    safe = result.get("safeSearchAnnotation", {})
    ratings = normalize_safety(
        [
            {"category": "adult", "probability": safe.get("adult", "UNKNOWN")},
            {"category": "spoof", "probability": safe.get("spoof", "UNKNOWN")},
            {"category": "medical", "probability": safe.get("medical", "UNKNOWN")},
            {"category": "violence", "probability": safe.get("violence", "UNKNOWN")},
            {"category": "racy", "probability": safe.get("racy", "UNKNOWN")},
        ]
    )
    return [
        {
            "category": item.category,
            "probability": item.probability,
            "blocked": item.blocked,
        }
        for item in ratings
    ]
