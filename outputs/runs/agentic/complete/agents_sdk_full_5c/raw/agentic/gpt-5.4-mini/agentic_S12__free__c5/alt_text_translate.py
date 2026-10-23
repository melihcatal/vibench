from __future__ import annotations

from typing import Optional

import requests

from vision_client import VisionClientConfig, load_vision_config

GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"


def translate_alt_text(text: str, target_language: str, config: Optional[VisionClientConfig] = None) -> str:
    config = config or load_vision_config()
    params = {"key": config.translate_api_key or config.google_api_key}
    payload = {"q": text, "target": target_language, "format": "text"}
    response = requests.post(GOOGLE_TRANSLATE_API_URL, params=params, json=payload, timeout=config.timeout_seconds)
    response.raise_for_status()
    return response.json()["data"]["translations"][0]["translatedText"]


__all__ = ["translate_alt_text"]
