import os
import deepl
from typing import List

def translate_text(text: str, target_language: str = "DE") -> str:
    """
    Translates text to a target language using the DeepL API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "DE" for German).

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
