from __future__ import annotations

import os

import requests


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def appeal_translate(
    text: str, target_lang: str = "EN-US", source_lang: str | None = None
) -> dict[str, str]:
    auth_key = os.environ.get("DEEPL_API_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_API_KEY is required")
    payload = {"text": [text], "target_lang": target_lang}
    if source_lang:
        payload["source_lang"] = source_lang
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        data=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    translation = data["translations"][0]
    return {
        "provider": "deepl",
        "translated_text": translation["text"],
        "detected_source_language": translation.get(
            "detected_source_language", source_lang or ""
        ),
        "target_language": target_lang,
    }
