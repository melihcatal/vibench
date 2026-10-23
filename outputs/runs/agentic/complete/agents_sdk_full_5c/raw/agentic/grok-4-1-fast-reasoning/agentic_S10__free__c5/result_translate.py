import os
import requests

def translate(text: str, target_lang: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]