import os
from typing import Optional
import deepl


def ocr_translate(
    text: str, target_lang: str = "EN", source_lang: Optional[str] = None
) -> str:
    """Translate extracted OCR text using DeepL API.

    Args:
        text: Text to translate
        target_lang: Target language code (e.g., 'EN', 'FR', 'DE')
        source_lang: Source language code (optional, auto-detected if None)

    Returns:
        Translated text
    """
    # Initialize DeepL translator
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    # Translate text
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )

    return result.text
