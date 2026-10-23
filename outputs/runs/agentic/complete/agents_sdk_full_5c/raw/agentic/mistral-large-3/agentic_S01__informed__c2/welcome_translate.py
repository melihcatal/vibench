# Translate onboarding copy into the user's locale using DeepL

import os
import deepl
from typing import Optional


def translate_welcome_message(text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
    """
    Translate onboarding text using DeepL API.
    Model: DeepL API Free or Pro (deepl.com).
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text