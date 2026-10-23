from __future__ import annotations

import os
from typing import Dict

from google.cloud import translate_v2

from observability_models import TranslationResult


def main(text: str | None = None, target_language: str | None = None) -> Dict[str, object]:
    text = text or os.getenv("LOG_TEXT", "")
    target_language = target_language or os.getenv("TARGET_LANGUAGE", "es")
    client = translate_v2.Client()
    translated = client.translate(text, target_language=target_language)
    result = TranslationResult(
        provider="google-cloud-translate-v2",
        source_text=text,
        translated_text=translated.get("translatedText", ""),
        target_language=target_language,
        raw_response=translated,
    )
    return {"provider": result.provider, "translated_text": result.translated_text, "target_language": result.target_language}
