import os
from typing import Optional
import deepl

def payload_translate(text: str, target_lang: str = "FR") -> str:
    """
    Translates customer-facing message payload text using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text