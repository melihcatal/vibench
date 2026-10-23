import deepl
import os
from typing import Dict, Any

# Initialize DeepL translator
translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def payload_translate(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates customer-facing message payload text using DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        str: The translated text.
    """
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
