import os
import requests

# Identify provider in code
PROVIDER = "DeepL"

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

BASE_URL = "https://api.deepl.com/v2/translate"


def translate_text(text: str, target_lang: str = "EN") -> str:
    params = {"auth_key": DEEPL_AUTH_KEY, "text": text, "target_lang": target_lang}
    response = requests.post(BASE_URL, data=params)
    response.raise_for_status()
    result = response.json()
    translated = result["translations"][0]["text"]
    return translated
