from __future__ import annotations

from typing import Optional

import requests

from vision_client import VisionClientConfig, build_image_data_uri, load_vision_config
from vision_models import SafetyScore, coerce_safety

GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def score_image_safety(image_path: str, config: Optional[VisionClientConfig] = None) -> SafetyScore:
    config = config or load_vision_config()
    image_uri = build_image_data_uri(image_path)
    payload = {
        "requests": [
            {
                "image": {"content": image_uri.split(",", 1)[1]},
                "features": [{"type": "SAFE_SEARCH_DETECTION", "maxResults": 1}],
            }
        ]
    }
    params = {"key": config.google_api_key} if config.google_api_key else {}
    response = requests.post(GOOGLE_VISION_API_URL, params=params, json=payload, timeout=config.timeout_seconds)
    response.raise_for_status()
    data = response.json()
    safe_search = data.get("responses", [{}])[0].get("safeSearchAnnotation", {})
    return coerce_safety(safe_search)


__all__ = ["score_image_safety"]
