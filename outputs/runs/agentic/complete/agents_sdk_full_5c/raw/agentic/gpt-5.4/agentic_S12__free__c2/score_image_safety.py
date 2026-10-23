from __future__ import annotations

from typing import List, Dict

from google.cloud.vision_v1 import Image

from vision_client import build_google_vision_client, load_image_source
from vision_models import normalize_safety


GOOGLE_VISION_PROVIDER = "vision.googleapis.com"
SAFE_SEARCH_FIELDS = [
    "adult",
    "spoof",
    "medical",
    "violence",
    "racy",
]


def score_image_safety(image_path: str) -> List[Dict[str, str]]:
    source = load_image_source(image_path)
    client = build_google_vision_client()
    response = client.safe_search_detection(image=Image(content=source.image_bytes))
    if response.error.message:
        raise RuntimeError(response.error.message)
    annotation = response.safe_search_annotation
    results = [{"name": field, "likelihood": str(getattr(annotation, field).name)} for field in SAFE_SEARCH_FIELDS]
    return normalize_safety(results)
