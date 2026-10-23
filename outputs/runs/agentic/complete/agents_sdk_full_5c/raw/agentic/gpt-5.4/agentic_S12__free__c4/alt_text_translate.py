from __future__ import annotations

from typing import Dict
from urllib.parse import urlencode

from vision_client import GOOGLE_TRANSLATE_ENDPOINT, get_env, post_json


PROVIDER = "google_cloud_translate"
MODEL = "nmt"


def alt_text_translate(text: str, target_language: str, source_language: str | None = None) -> Dict[str, str]:
    api_key = get_env("GOOGLE_API_KEY")
    url = f"{GOOGLE_TRANSLATE_ENDPOINT}?{urlencode({'key': api_key})}"
    payload = {
        "q": text,
        "target": target_language,
        "format": "text",
        "model": MODEL,
    }
    if source_language:
        payload["source"] = source_language
    response = post_json(url, payload)
    translation = response["data"]["translations"][0]
    return {
        "provider": PROVIDER,
        "model": MODEL,
        "translated_text": translation["translatedText"],
        "detected_source_language": translation.get("detectedSourceLanguage", source_language or ""),
        "target_language": target_language,
    }
