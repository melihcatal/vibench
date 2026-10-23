import os
import requests

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

def translate_payload(payload_text: str, target_lang: str = "ES") -> str:
    params = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": payload_text,
        "target_lang": target_lang
    }
    response = requests.post(DEEPL_URL, data=params)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]