from __future__ import annotations

import os

from google.cloud import translate_v2 as translate

from model_models import TranslationResult


TARGET_LANGUAGE = os.environ.get("TARGET_LANGUAGE", "es")


def localize_platform_output(text: str, target_locale: str = TARGET_LANGUAGE) -> TranslationResult:
    client = translate.Client()
    result = client.translate(text, target_language=target_locale)
    return TranslationResult(
        source_text=text,
        translated_text=result["translatedText"],
        target_locale=target_locale,
        provider="google-cloud-translation",
        raw=result,
    )
