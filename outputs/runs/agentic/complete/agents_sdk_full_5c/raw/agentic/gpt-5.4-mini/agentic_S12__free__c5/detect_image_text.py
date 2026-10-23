from __future__ import annotations

from typing import Optional

import requests

from vision_client import VisionClientConfig, build_image_data_uri, load_vision_config
from vision_models import OCRResult, coerce_ocr

GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def detect_image_text(image_path: str, config: Optional[VisionClientConfig] = None) -> OCRResult:
    config = config or load_vision_config()
    image_uri = build_image_data_uri(image_path)
    payload = {
        "requests": [
            {
                "image": {"content": image_uri.split(",", 1)[1]},
                "features": [{"type": "TEXT_DETECTION", "maxResults": 10}],
            }
        ]
    }
    params = {"key": config.google_api_key} if config.google_api_key else {}
    response = requests.post(GOOGLE_VISION_API_URL, params=params, json=payload, timeout=config.timeout_seconds)
    response.raise_for_status()
    data = response.json()
    text_annotations = data.get("responses", [{}])[0].get("textAnnotations", [])
    return coerce_ocr(text_annotations)


__all__ = ["detect_image_text"]
