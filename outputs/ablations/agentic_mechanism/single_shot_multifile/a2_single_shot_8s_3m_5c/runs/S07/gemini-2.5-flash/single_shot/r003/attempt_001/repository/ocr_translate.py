import os
from typing import Optional

from document_client import get_deepl_translator
from document_models import TranslationInput, TranslationOutput

def translate_ocr_text(
    translation_input: TranslationInput,
) -> TranslationOutput:
    """Translates extracted OCR text using DeepL API."""
    translator = get_deepl_translator()

    # DeepL target_lang expects ISO 639-1 code (e.g., 'en', 'fr') or language with country code (e.g., 'en-US')
    result = translator.translate_text(
        translation_input.text,
        target_lang=translation_input.target_lang,
        source_lang=translation_input.source_lang
    )

    translated_text = result.text
    detected_source_lang = result.detected_source_lang if hasattr(result, 'detected_source_lang') else None

    return TranslationOutput(translated_text=translated_text, detected_source_lang=detected_source_lang)
