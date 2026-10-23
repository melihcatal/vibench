# localized_platform_output.py
# [LATER-STEP] Translate platform model output for another locale using DeepL

# Provider: DeepL (translation API)
import os
import requests
from typing import Tuple

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")

BASE_URL = "https://api.deepl.com/v2/translate"


def translate_text(text: str, target_lang: str = "EN") -> str:
    """Translate text to the specified target language using DeepL."""
    payload = {"text": text, "target_lang": target_lang, "auth_key": DEEPL_AUTH_KEY}
    response = requests.post(BASE_URL, data=payload)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]


if __name__ == "__main__":
    # Example: translate a watsonx.ai output to French
    raw_output = "The quick brown fox jumps over the lazy dog."
    french = translate_text(raw_output, target_lang="FR")
    print(f"Original: {raw_output}\nTranslated: {french}")
