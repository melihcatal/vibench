import os
import requests
from typing import Optional


def translate_consent_text(text: str, target_lang: str, api_key: Optional[str] = None) -> str:
    api_key = api_key or os.getenv("DEEPL_API_KEY")
    
    response = requests.post(
        url="https://api-free.deepl.com/v2/translate",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"DeepL-Auth-Key {api_key}",
        },
        json={
            "text": [text],
            "target_lang": target_lang,
        },
    )
    response.raise_for_status()
    
    return response.json()["translations"][0]["text"]