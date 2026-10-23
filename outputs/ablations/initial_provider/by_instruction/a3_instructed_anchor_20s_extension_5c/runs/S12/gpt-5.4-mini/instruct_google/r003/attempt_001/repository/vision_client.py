import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class VisionConfig:
    google_vision_api_key: str
    google_vision_api_url: str = "https://vision.googleapis.com/v1/images:annotate"


def load_config() -> VisionConfig:
    api_key = os.getenv("GOOGLE_VISION_API_KEY") or os.getenv("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_VISION_API_KEY is required")
    return VisionConfig(google_vision_api_key=api_key)


def image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("ascii")


def post_google_vision(request_body: Dict[str, Any], config: Optional[VisionConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    response = requests.post(
        cfg.google_vision_api_url,
        params={"key": cfg.google_vision_api_key},
        json=request_body,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
