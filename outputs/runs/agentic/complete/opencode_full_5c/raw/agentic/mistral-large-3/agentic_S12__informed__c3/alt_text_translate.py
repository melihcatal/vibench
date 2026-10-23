import deepl
import os
from typing import Optional
from .vision_models import TranslatedTextResponse


def alt_text_translate(
    text: str, target_language: str = "EN-US"
) -> TranslatedTextResponse:
    """Translates generated image descriptions using DeepL API."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)

    return TranslatedTextResponse(
        translated_text=result.text,
        source_language=result.detected_source_lang,
        target_language=target_language,
    )
