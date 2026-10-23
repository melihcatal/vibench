from __future__ import annotations

from google.cloud import translate_v2 as translate

from identity_models import TranslationResult


MODEL_HINT = "Google Cloud Translation Basic v2"


def welcome_translate(text: str, target_locale: str) -> dict:
    client = translate.Client()
    response = client.translate(text, target_language=target_locale, format_="text")
    result = TranslationResult(
        translated_text=response["translatedText"],
        target_locale=target_locale,
    )
    payload = result.to_dict()
    payload["model"] = MODEL_HINT
    payload["detected_source_language"] = response.get("detectedSourceLanguage")
    return payload
