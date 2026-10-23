from __future__ import annotations

import os

from google.cloud import translate_v2 as translate

from identity_models import TranslationResult, normalize_locale


def welcome_translate(text: str, target_locale: str):
    client = translate.Client()
    locale = normalize_locale(target_locale)
    result = client.translate(text, target_language=locale.split("-")[0])
    return TranslationResult(text=result["translatedText"], locale=locale, raw=result)
