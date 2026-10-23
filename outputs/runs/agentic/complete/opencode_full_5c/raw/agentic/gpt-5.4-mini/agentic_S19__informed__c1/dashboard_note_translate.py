from typing import Any, Dict

import requests


def dashboard_note_translate(text: str, target_locale: str) -> Dict[str, Any]:
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={
            "auth_key": __import__("os").environ["DEEPL_AUTH_KEY"],
            "text": text,
            "target_lang": target_locale.upper(),
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
