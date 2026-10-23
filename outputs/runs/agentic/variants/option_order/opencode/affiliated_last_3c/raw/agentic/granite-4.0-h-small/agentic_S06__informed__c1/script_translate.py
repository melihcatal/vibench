from __future__ import annotations

from typing import Optional
import requests
import os

# Configuration (prefer env vars)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")  # required for DeepL API
TARGET_LANG = os.getenv("TRANSLATION_TARGET", "es")  # default target language (Spanish)

BASE_URL = "https://api.deepl.com/v2/translate"


def translate_text(source_text: str, target_lang: Optional[str] = None) -> str:
    """
    Translate plain text using DeepL API.
    Requires the environment variable DEEPL_AUTH_KEY to be set.
    Returns the translated string.
    """
    if not DEEPL_AUTH_KEY:
        raise RuntimeError("Set DEEPL_AUTH_KEY env var before translating.")

    params = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": source_text,
        "target_lang": target_lang or TARGET_LANG,
    }
    response = requests.post(BASE_URL, data=params)
    response.raise_for_status()
    data = response.json()
    translated = data["translations"][0]["text"]
    return translated


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(translate_text("Hello world"))
