from __future__ import annotations

import os
from typing import Any, Dict

import requests


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def dashboard_note_translate(
    text: str, target_lang: str, source_lang: str | None = None
) -> Dict[str, Any]:
    payload = {"text": [text], "target_lang": target_lang}
    if source_lang:
        payload["source_lang"] = source_lang
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}"},
        data=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()["translations"][0]
    return {
        "translated_text": data["text"],
        "detected_source_language": data.get("detected_source_language", source_lang),
        "target_language": target_lang,
    }
