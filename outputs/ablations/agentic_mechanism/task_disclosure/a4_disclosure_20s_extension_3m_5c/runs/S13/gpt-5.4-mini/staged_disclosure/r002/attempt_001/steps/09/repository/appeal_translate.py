import os
from typing import Optional

import requests


GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"


def translate_appeal_text(text: str, target_language: str = "en", source_language: Optional[str] = None) -> str:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_TRANSLATE_API_KEY is required")

    params = {"key": api_key}
    payload = {"q": text, "target": target_language, "format": "text"}
    if source_language:
        payload["source"] = source_language

    response = requests.post(GOOGLE_TRANSLATE_ENDPOINT, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["data"]["translations"][0]["translatedText"]


if __name__ == "__main__":
    import sys

    appeal_text = sys.stdin.read()
    print(translate_appeal_text(appeal_text))
