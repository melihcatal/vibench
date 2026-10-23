import os
from google.cloud import translate_v2 as translate
from observability_models import TranslationResult


def translate_note(text: str, target_locale: str) -> TranslationResult:

    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_locale)

    return TranslationResult(
        original_text=text,
        translated_text=result["translatedText"],
        target_locale=target_locale,
        source_locale=result["detectedSourceLanguage"],
    )
