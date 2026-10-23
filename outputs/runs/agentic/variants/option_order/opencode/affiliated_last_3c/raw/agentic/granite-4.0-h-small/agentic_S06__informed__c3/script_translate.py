import os
from typing import Optional
import requests

# Configuration constants -- set via env vars before invoking
TRANSLATE_API_KEY = os.getenv("DEEPL_AUTH_KEY")
ENDPOINT = "https://api.deepl.com/v2/translate"

if not TRANSLATE_API_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")


def translate_text(text: str, target_lang: str = "EN") -> str:
    """Translate plain narration script using DeepL API and return translated string."""
    params = {"auth_key": TRANSLATE_API_KEY, "text": text, "target_lang": target_lang}
    resp = requests.get(ENDPOINT, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data["translations"][0]["text"]
