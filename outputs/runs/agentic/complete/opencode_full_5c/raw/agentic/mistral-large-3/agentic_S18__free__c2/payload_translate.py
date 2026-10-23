import requests
import os

# Provider: DeepL API
# Identifiable by: DEEPL_API_KEY, api-free.deepl.com
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def payload_translate(text: str, target_lang: str = "EN") -> str:
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"text": [text], "target_lang": target_lang}

    response = requests.post(DEEPL_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["translations"][0]["text"]
