import os
import requests
from typing import Any

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if DEEPL_AUTH_KEY:
    DEEPL_URL = "https://api-free.deepl.com/v2/translate"
else:
    DEEPL_URL = "https://api.deepl.com/v2/translate"  # pro

def translate_result(text: str, target_lang: str = "EN-US") -> str:
    \"\"\"Translate model output using DeepL API.\"\"\"
    data: dict[str, Any] = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": text,
        "target_lang": target_lang.upper()
    }
    response = requests.post(DEEPL_URL, data=data)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]