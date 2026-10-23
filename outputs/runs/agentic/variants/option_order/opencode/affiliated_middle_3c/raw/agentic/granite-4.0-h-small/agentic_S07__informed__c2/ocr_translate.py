# ocr_translate.py
# LATER-STEP file
# Translates extracted OCR plain-text using DeepL SDK

import os
from deepl import DeepL
from document_models import TranslationResult

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")

deepl_client = DeepL(auth_key=DEEPL_AUTH_KEY)


def translate_text(source_text: str, target_lang: str = "EN") -> TranslationResult:
    """Translate OCR-extracted text using DeepL API.

    Args:
        source_text: Text extracted from document image.
        target_lang: ISO language code of target language (default EN).

    Returns:
        TranslationResult object with translated text.
    """
    result = deepl_client.translate_text(text=source_text, target_lang=target_lang)
    return TranslationResult(
        translated_text=result.translations[0].text,
        source_lang=result.source_lang,
        target_lang=result.target_lang,
    )
