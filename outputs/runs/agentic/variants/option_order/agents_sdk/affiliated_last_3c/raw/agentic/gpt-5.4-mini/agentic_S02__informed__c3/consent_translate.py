from __future__ import annotations

import os

from deepl import Translator

from identity_models import TranslationResult


TRANSLATOR = Translator(auth_key=os.getenv("DEEPL_AUTH_KEY", ""))


def consent_translate(text: str, target_language: str = "ES") -> TranslationResult:
    result = TRANSLATOR.translate_text(text, target_lang=target_language)
    return TranslationResult(
        source_text=text,
        translated_text=str(result),
        source_language=getattr(result, "detected_source_lang", None),
        target_language=target_language,
        provider="DeepL",
    )
