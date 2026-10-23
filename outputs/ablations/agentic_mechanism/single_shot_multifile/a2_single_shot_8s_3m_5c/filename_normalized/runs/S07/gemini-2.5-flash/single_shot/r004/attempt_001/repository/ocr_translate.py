import os
import deepl
from document_client import get_deepl_translator
from document_models import TranslationResult

def translate_ocr_text(text: str, target_language: str = "en", source_language: str = "auto") -> TranslationResult:
    translator = get_deepl_translator()

    if source_language == "auto":
        result = translator.translate_text(text, target_lang=target_language)
    else:
        result = translator.translate_text(text, source_lang=source_language, target_lang=target_language)

    return TranslationResult(
        translated_text=result.text,
        source_language=result.detected_source_lang,
        target_language=target_language
    )