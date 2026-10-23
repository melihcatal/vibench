# result_translate.py
# [LATER-STEP]
"""Translates generated model output into another language or format.

Illustrates usage of a concrete hosted translation model (e.g.,
DeepL or OpenAI's translation endpoint). The helper normalizes input
and returns the translated text.

NOTE: Replace placeholders with real API keys or endpoints for
production use.
"""

import os
import requests
from typing import Dict, Any

# Example: DeepL PRO API (requires auth token in environment)
DEEPL_AUTH_TOKEN = os.getenv("DEEPL_AUTH_TOKEN", "demo_token")
BASE_URL = "https://api.deepl.com/v2/translate"


def translate_text(
    source_text: str,
    target_lang: str = "EN",
) -> str:
    """
    Translates a piece of text from the source language (detected automatically)
    to the requested target language code (such as 'EN', 'FR', 'DE', etc.).

    Args:
        source_text (str): Text to translate.
        target_lang (str): Two‑letter language code or language name.
    Returns:
        str: Translated text.
    """
    payload = {
        "text": source_text,
        "target_lang": target_lang,
    }
    headers = {
        "Authorization": f"Bearer {DEEPL_AUTH_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(BASE_URL, data=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    # DeepL returns a list of translations; pick the first.
    return result["translations"][0]["text"]


# Example usage (commented out to avoid accidental execution on import)
# if __name__ == '__main__':
#     print(translate_text('Bonjour le monde!', target_lang='EN'))
