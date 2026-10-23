# LATER-STEP: script_translate.py
# Translate narration script before synthesis using DeepL API

import os
import json
import requests
from typing import Dict, Any

# Load credentials from environment variables (ensure they are set before running)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_ENDPOINT = "https://api.deepl.com/v2/translate"


def translate_text(
    text: str,
    target_lang: str = "de",  # default target language: German ('de')
) -> str:
    """Translate plain text using DeepL API.

    Args:
        text: Source text to translate.
        target_lang: ISO language code for target language.

    Returns:
        Translated text string.
    """
    payload = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": text,
        "target_lang": target_lang,
    }
    response = requests.post(DEEPL_ENDPOINT, data=payload)
    response.raise_for_status()
    data = response.json()
    # DeepL returns JSON like { 'translations': [{'text': '...'}] }
    return data["translations"][0]["text"]


# Example usage (requires credentials env vars)
if __name__ == "__main__":
    sample = "Hello, this script will be translated."
    translated = translate_text(sample, target_lang="de")
    print("Original:", sample)
    print("Translated (de):", translated)
