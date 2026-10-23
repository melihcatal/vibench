import os
import requests
from typing import Dict, Any

DEEPL_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_identity_consent(text: str, target_lang: str = "EN") -> str:
    data: Dict[str, Any] = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": text,
        "target_lang": target_lang.upper(),
    }
    resp = requests.post(DEEPL_URL, data=data)
    resp.raise_for_status()
    translations = resp.json()["translations"]
    return translations[0]["text"]
