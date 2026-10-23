from __future__ import annotations

import os

from google.cloud import translate_v2 as translate

from identity_models import TranslationResult


def welcome_translate(text: str, locale: str) -> dict:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    client = translate.Client(project=project_id)
    response = client.translate(text, target_language=locale, format_="text")
    return TranslationResult(locale=locale, translated_text=response["translatedText"]).__dict__
