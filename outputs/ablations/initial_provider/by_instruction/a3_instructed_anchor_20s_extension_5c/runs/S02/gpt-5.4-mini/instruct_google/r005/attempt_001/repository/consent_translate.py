from typing import Dict

import requests


def translate_consent_copy(text: str, target_language: str) -> str:
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        headers={"Authorization": f"Bearer {__import__('os').environ['GOOGLE_TRANSLATE_ACCESS_TOKEN']}"},
        json={"q": text, "target": target_language, "format": "text"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["data"]["translations"][0]["translatedText"]
