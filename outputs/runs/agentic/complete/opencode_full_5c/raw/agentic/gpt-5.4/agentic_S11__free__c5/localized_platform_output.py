from __future__ import annotations

import os
from typing import Any, Dict

import requests


def localized_platform_output(text: str, target_locale: str) -> Dict[str, Any]:
    api_key = os.environ["DEEPL_API_KEY"]
    response = requests.post(
        "https://api.deepl.com/v2/translate",
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data={
            "text": text,
            "target_lang": target_locale.upper(),
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translation = data["translations"][0]
    return {
        "text": translation.get("text", ""),
        "detected_source_language": translation.get("detected_source_language"),
        "raw_response": data,
    }
