import os
from typing import Dict, Any
import deepl

def translate_text(
    text: str,
    target_lang: str = "EN-US",
    source_lang: str = None,
) -> str:
    """
    Translate text using DeepL API.
    
    Args:
        text: Input text to translate.
        target_lang: Target language code (e.g., "EN-US", "DE", "FR").
        source_lang: Optional source language code.
    
    Returns:
        Translated text as a string.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
    )
    return result.text