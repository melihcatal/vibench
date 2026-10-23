import deepl
import os
from typing import Optional
from document_models import TranslationResponse


def translate_text(text: str, target_lang: str = "EN-US") -> TranslationResponse:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set in the environment.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)

    return TranslationResponse(
        translated_text=result.text,
        detected_language=result.detected_source_lang,
        target_language=target_lang
    )