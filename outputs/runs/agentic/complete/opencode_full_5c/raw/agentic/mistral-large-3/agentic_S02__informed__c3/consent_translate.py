from typing import Dict, Any
import os
from deepl import Translator

# DeepL API for translation
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def consent_translate(text: str, target_lang: str = "EN-US") -> str:
    """Translate identity-provider consent copy using DeepL."""
    translator = Translator(auth_key=DEEPL_AUTH_KEY)

    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
