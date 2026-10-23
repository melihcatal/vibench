# [LATER-STEP] appeal_translate.py

import os
from typing import Any

# Using the DeepL API as the concrete translation service.
# The environment variable DEEPL_AUTH_KEY must be set with a valid auth key.


def translate_appeal(text: str, target_lang: str = "en") -> str:
    """Translate an appeal/note for reviewer handling.

    Calls the DeepL API (sdk interface) and returns the translated string.
    Adjust `target_lang` as needed (e.g., 'en', 'es', 'de').
    """
    try:
        from deepl import DeepL, TranslateParams
    except ImportError:
        raise RuntimeError(
            "DeepL SDK not installed. Run `pip install deepl` to enable translation."
        )
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Environment variable DEEPL_AUTH_KEY must be set.")
    client = DeepL(auth_key=auth_key)
    result = client.translate(text, target_lang=target_lang)
    # The SDK returns a dict; extract the translated_text field.
    return result.get("text", text)
