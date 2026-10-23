import os

import requests


def appeal_translate(payload, config=None):
    text = payload["text"] if isinstance(payload, dict) else str(payload)
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": (config or {}).get("api_key") or os.environ["GOOGLE_TRANSLATE_API_KEY"]},
        json={"q": text, "target": (config or {}).get("target", "en"), "format": "text"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
