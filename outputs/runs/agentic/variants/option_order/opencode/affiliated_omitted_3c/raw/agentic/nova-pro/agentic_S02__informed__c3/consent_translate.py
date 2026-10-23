import os
import requests

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_consent(text):
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}"}
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        headers=headers,
        json={"text": text, "target_lang": "EN"},
    )
    return response.json()
