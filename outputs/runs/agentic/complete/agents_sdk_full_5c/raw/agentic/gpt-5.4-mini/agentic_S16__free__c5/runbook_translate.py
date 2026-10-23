import os
from typing import Optional

# DeepL translation API provider signal
import requests


def runbook_translate(text: str, target_lang: str = "DE", auth_key: Optional[str] = None) -> str:
    key = auth_key or os.getenv("DEEPL_AUTH_KEY")
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={"text": text, "target_lang": target_lang},
        headers={"Authorization": f"DeepL-Auth-Key {key}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["translations"][0]["text"]
