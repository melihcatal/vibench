import os
import requests
from typing import Dict

# Provider identification – translation (DeepL) in this example
translation_provider = "deepl"

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
BASE_TRANSLATE_URL = "https://api.deepl.com/v2/translate"


def translate_field(original_text: str, target_lang: str = "fr") -> Dict[str, Any]:
    """
    Translate a single text field (e.g., `description`) into the target language.
    Returns a dict containing the original text, the translated text, and any API status.
    """
    params = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": original_text,
        "target_lang": target_lang,
    }
    resp = requests.post(BASE_TRANSLATE_URL, data=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    translated = data.get("translations", [{}])[0].get("text")
    return {
        "original_text": original_text,
        "target_lang": target_lang,
        "translated_text": translated,
    }
