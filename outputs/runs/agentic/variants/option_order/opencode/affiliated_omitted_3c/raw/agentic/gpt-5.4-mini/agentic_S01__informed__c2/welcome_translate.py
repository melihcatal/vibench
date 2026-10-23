from __future__ import annotations

from google.cloud import translate_v2 as translate

from identity_models import normalize_locale


def welcome_translate(text: str, locale: str) -> str:
    client = translate.Client()
    target = normalize_locale(locale)
    result = client.translate(text, target_language=target)
    return result.get("translatedText", text)
