from __future__ import annotations

import os

from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_language: str, source_language: str | None = None) -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language, source_language=source_language)
    return result.get("translatedText", "")


def default_locale_copy(locale: str | None) -> str:
    client = translate.Client()
    text = os.getenv("WELCOME_COPY", "Welcome to your new account.")
    result = client.translate(text, target_language=(locale or "en"))
    return result.get("translatedText", text)
