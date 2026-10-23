from __future__ import annotations

import base64
import os
from typing import Any, Dict, List, Optional

import requests

from vision_client import VisionClientConfig, build_image_data_uri, load_vision_config
from vision_models import ImageLabelResult, coerce_labels


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def detect_image_labels(image_path: str, max_results: int = 10, config: Optional[VisionClientConfig] = None) -> ImageLabelResult:
    config = config or load_vision_config()
    image_uri = build_image_data_uri(image_path)
    payload: Dict[str, Any] = {
        "requests": [
            {
                "image": {"content": image_uri.split(",", 1)[1]},
                "features": [{"type": "LABEL_DETECTION", "maxResults": max_results}],
            }
        ]
    }
    params = {"key": config.google_api_key} if config.google_api_key else {}
    response = requests.post(GOOGLE_VISION_API_URL, params=params, json=payload, timeout=config.timeout_seconds)
    response.raise_for_status()
    data = response.json()
    annotations = data.get("responses", [{}])[0].get("labelAnnotations", [])
    return coerce_labels(annotations)


__all__ = ["detect_image_labels"]
