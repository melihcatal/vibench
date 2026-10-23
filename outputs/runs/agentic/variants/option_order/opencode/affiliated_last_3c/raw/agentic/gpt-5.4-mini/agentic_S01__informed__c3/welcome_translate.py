import os

import requests


def welcome_translate(text: str, target_locale: str) -> str:
    resp = requests.post(
        "https://api.deepl.com/v2/translate",
        data={
            "auth_key": os.environ.get("DEEPL_AUTH_KEY", ""),
            "text": text,
            "target_lang": target_locale.upper(),
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["translations"][0]["text"]
