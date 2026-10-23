import os
import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = os.getenv("DEEPL_AUTH_KEY", "")


def translate_script(text: str, target_lang: str = "EN-US") -> str:
    r = requests.post(DEEPL_API_URL, data={"auth_key": DEEPL_API_KEY, "text": text, "target_lang": target_lang})
    r.raise_for_status()
    return r.json()["translations"][0]["text"]
