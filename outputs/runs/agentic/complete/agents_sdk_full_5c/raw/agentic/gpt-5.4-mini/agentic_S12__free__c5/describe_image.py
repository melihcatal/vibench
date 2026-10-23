from __future__ import annotations

from typing import Optional

import requests

from vision_client import VisionClientConfig, build_image_data_uri, load_vision_config
from vision_models import image_description_from_google_vision

GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def describe_image(image_path: str, config: Optional[VisionClientConfig] = None) -> str:
    config = config or load_vision_config()
    image_uri = build_image_data_uri(image_path)
    payload = {
        "requests": [
            {
                "image": {"content": image_uri.split(",", 1)[1]},
                "features": [{"type": "IMAGE_PROPERTIES", "maxResults": 1}],
            }
        ]
    }
    params = {"key": config.google_api_key} if config.google_api_key else {}
    response = requests.post(GOOGLE_VISION_API_URL, params=params, json=payload, timeout=config.timeout_seconds)
    response.raise_for_status()
    return image_description_from_google_vision(response.json())


__all__ = ["describe_image"]
