from __future__ import annotations

import os
from typing import Dict

import requests


DEEPL_API_KEY_ENV = "DEEPL_API_KEY"
DEEPL_TRANSLATE_URL = "https://api.deepl.com/v2/translate"


def translate_consent_copy(
    text: str, target_lang: str, source_lang: str | None = None
) -> Dict[str, str]:
    data = {"text": [text], "target_lang": target_lang}
    if source_lang:
        data["source_lang"] = source_lang
    response = requests.post(
        DEEPL_TRANSLATE_URL,
        headers={"Authorization": f"DeepL-Auth-Key {os.environ[DEEPL_API_KEY_ENV]}"},
        data=data,
        timeout=30,
    )
    response.raise_for_status()
    translation = response.json()["translations"][0]
    return {
        "provider": "deepl",
        "translated_text": translation["text"],
        "detected_source_language": translation.get(
            "detected_source_language", source_lang or ""
        ),
        "target_language": target_lang,
    }
