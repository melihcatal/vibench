import os

import requests


def invoice_note_translate(payload, config=None):
    config = config or {}
    target_language = config.get("target_language", "en")
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": os.environ.get("GOOGLE_TRANSLATE_API_KEY")},
        json={"q": payload["text"], "target": target_language, "format": "text"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
