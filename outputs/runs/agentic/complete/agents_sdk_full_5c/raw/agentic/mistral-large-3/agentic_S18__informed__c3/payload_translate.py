# Translate customer-facing message payload text using DeepL API
import deepl
import os


def translate_payload(text: str, target_lang: str = "EN-US") -> str:
    """Translate text using DeepL API."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text