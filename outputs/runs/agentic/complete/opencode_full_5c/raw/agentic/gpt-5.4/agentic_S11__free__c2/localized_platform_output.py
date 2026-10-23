from __future__ import annotations

import os
from typing import Any, Dict

import requests


DEEPL_API_URL = os.getenv("DEEPL_API_URL", "https://api.deepl.com/v2/translate")


def localized_platform_output(text: str, target_lang: str) -> Dict[str, Any]:
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}"},
        data={"text": text, "target_lang": target_lang},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    translation = body["translations"][0]
    return {
        "text": translation["text"],
        "detected_source_language": translation.get("detected_source_language"),
        "provider": "deepl",
        "raw": body,
    }
