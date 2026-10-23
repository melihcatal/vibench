import os
from typing import Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_result(text: str, target_lang: str = "EN-US", source_lang: Optional[str] = None) -> str:
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    data = {"text": text, "target_lang": target_lang}
    if source_lang:
        data["source_lang"] = source_lang

    response = requests.post(
        DEEPL_API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    if not translations:
        raise RuntimeError("No translation returned by DeepL")
    return translations[0]["text"]
