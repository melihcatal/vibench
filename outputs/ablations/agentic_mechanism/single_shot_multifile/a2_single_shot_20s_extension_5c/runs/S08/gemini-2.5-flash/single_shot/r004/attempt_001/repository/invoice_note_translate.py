import os
import deepl
from document_client import get_deepl_translator
from typing import Optional

def translate_invoice_note_deepl(text: str, target_lang: str = "EN-US") -> Optional[str]:
    """
    Translates extracted invoice notes or descriptions using DeepL API.
    Requires DEEPL_API_KEY environment variable.
    Target languages can be "EN-US", "ES", "FR", "DE", etc.
    See DeepL API documentation for full list of supported target languages.
    """
    if not text:
        return None

    translator = get_deepl_translator()

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.exceptions.DeepLException as e:
        print(f"DeepL translation error: {e}")
        return None
