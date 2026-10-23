import os
import requests

DEEPL_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

def translate_consent_copy(text: str, source_lang: str = "auto", target_lang: str = "en-US") -> str:
    data = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    response = requests.post(DEEPL_URL, data=data)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]