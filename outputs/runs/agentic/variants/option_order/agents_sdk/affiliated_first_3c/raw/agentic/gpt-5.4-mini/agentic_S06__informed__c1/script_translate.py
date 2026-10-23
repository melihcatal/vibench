from __future__ import annotations

import os

from google.cloud import translate_v2 as translate

from speech_models import normalize_text


def translate_script(text: str, target_language: str, source_language: str | None = None) -> str:
    client = translate.Client()
    payload = normalize_text(text)
    result = client.translate(payload, target_language=target_language, source_language=source_language)
    return result["translatedText"]


def translator_project() -> str | None:
    return os.getenv("GOOGLE_CLOUD_PROJECT")
