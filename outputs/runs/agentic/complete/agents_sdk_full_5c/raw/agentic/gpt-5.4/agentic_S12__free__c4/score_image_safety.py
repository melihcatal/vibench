from __future__ import annotations

from typing import Dict, Optional

from vision_client import build_vision_image, get_google_vision_client
from vision_models import normalize_safety_categories


PROVIDER = "google_cloud_vision"


def score_image_safety(image_path: Optional[str] = None, image_uri: Optional[str] = None) -> Dict[str, object]:
    client = get_google_vision_client()
    image = build_vision_image(image_path=image_path, image_uri=image_uri)
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation
    categories = {
        "adult": safe.adult.name,
        "medical": safe.medical.name,
        "spoof": safe.spoof.name,
        "violence": safe.violence.name,
        "racy": safe.racy.name,
    }
    return {"provider": PROVIDER, "categories": normalize_safety_categories(categories)}
