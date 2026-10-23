import os
import deepl
from typing import Optional

def translate_script(text: str, target_language: str) -> Optional[str]:
    """
    Translates a script to a target language using the DeepL API.

    Args:
        text: The source text to translate.
        target_language: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text, or None if an error occurs.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return None
