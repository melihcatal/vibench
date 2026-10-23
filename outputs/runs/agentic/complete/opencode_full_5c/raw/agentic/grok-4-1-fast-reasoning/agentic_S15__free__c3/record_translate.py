import requests
import os
from typing import Optional

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"


def translate_text(text: str, target_lang: str = "EN") -> Optional[str]:
    params = {"auth_key": DEEPL_API_KEY, "text": text, "target_lang": target_lang}
    response = requests.post(DEEPL_URL, data=params)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    return None
