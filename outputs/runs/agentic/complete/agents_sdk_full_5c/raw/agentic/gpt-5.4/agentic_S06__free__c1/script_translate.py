from __future__ import annotations

from typing import Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_script(text: str, target_lang: str, auth_key: str, source_lang: Optional[str] = None) -> str:
    payload = {
        "text": [text],
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        payload["source_lang"] = source_lang.upper()
    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    return body["translations"][0]["text"]
