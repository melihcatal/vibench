import os
from typing import Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_payload_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    data = {"text": text, "target_lang": target_language.upper()}
    if source_language:
        data["source_lang"] = source_language.upper()

    response = requests.post(
        DEEPL_API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    if not translations:
        raise RuntimeError("No translation returned by DeepL")
    return translations[0]["text"]
