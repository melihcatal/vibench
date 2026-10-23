import os
import json
import requests
from typing import Dict, Any

# DeepL API (provider identifiable) configuration
DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

TARGET_LANG = "fr"  # Example target language


def translate_text(text: str) -> str:
    """Translate text to the target language using DeepL API.

    Args:
        text (str): Source text to translate.

    Returns:
        str: Translated text.
    """
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}"}
    data = {"text": text, "target_lang": TARGET_LANG}
    try:
        resp = requests.post(DEEPL_API_URL, headers=headers, data=data, timeout=5)
        resp.raise_for_status()
        result = resp.json()
        return result["translations"][0]["text"]
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # fallback to original text


if __name__ == "__main__":
    sample_payload = {"content": "Hello, how are you?"}
    translated = translate_text(sample_payload["content"])
    print(f"Translated: {translated}")
