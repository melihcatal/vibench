import os

import requests


def dashboard_note_translate(text, target_language):
    key = os.getenv("DEEPL_AUTH_KEY")
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={"auth_key": key, "text": text, "target_lang": target_language},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
