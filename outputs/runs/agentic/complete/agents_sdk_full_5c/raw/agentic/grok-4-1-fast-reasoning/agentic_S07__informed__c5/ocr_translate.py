import os
import deepl
from typing import Optional

def ocr_translate(text: str, source_lang: Optional[str] = None, target_lang: str = 'EN') -> str:
    """
    Translate extracted OCR text using DeepL API.
    """
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text
