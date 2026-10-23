from __future__ import annotations

from typing import Any, Dict

import requests

from messaging_client import TRANSLATE_API_BASE, google_translate_params
from messaging_models import ensure_text


def payload_translate(payload: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    text = ensure_text(payload.get("text") or payload.get("message") or payload)
    response = requests.post(
        TRANSLATE_API_BASE,
        params=google_translate_params(),
        json={"q": text, "target": target_language, "format": "text"},
        timeout=30,
    )
    response.raise_for_status()
    translated = response.json()["data"]["translations"][0]
    return {
        "provider": "google_translate",
        "target_language": target_language,
        "translated_text": translated.get("translatedText", ""),
        "detected_source_language": translated.get("detectedSourceLanguage"),
    }
