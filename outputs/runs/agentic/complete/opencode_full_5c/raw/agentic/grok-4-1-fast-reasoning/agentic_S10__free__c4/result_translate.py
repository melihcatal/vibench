import os
import requests
from typing import Optional


def translate_result(
    text: str, target_lang: str = "EN", source_lang: Optional[str] = None
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        data["source_lang"] = source_lang
    response = requests.post(url, data=data)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]
