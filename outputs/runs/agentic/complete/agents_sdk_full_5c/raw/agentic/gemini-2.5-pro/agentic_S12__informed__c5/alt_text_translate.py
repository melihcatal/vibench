"""
[LATER-STEP] alt_text_translate.py - Translate generated image descriptions
"""
import os
import deepl
from typing import Optional

def translate_text(text: str, target_lang: str = "DE") -> Optional[str]:
    """
    Translates text to a target language using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None
