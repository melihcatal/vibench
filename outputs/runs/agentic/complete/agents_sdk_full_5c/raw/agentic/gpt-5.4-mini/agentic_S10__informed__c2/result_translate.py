import os
from model_models import TranslationResult
from deep_translator import GoogleTranslator

TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "es")


def translate_result(text: str, source_language: str = "auto", target_language: str = TARGET_LANGUAGE) -> TranslationResult:
    translated = GoogleTranslator(source=source_language, target=target_language).translate(text)
    return TranslationResult(
        source_text=text,
        translated_text=translated,
        source_language=source_language,
        target_language=target_language,
    )
