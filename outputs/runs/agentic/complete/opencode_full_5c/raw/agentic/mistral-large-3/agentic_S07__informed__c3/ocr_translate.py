import deepl
import os
from typing import Optional
from document_models import OCRResponse


def ocr_translate(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates extracted OCR text using DeepL API.

    Args:
        text: Extracted OCR text to translate.
        target_lang: Target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        Translated text as a string.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DeepL API key not configured.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
