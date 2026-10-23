from __future__ import annotations

import os

from google.cloud import translate_v2 as translate

from document_models import TranslationResult, normalize_text


def translate_ocr_text(text: str, target_language: str = "en") -> TranslationResult:
    client = translate.Client()
    response = client.translate(text, target_language=target_language)
    translated_text = normalize_text(response.get("translatedText"))
    return TranslationResult(
        source_text=text,
        translated_text=translated_text,
        source_language=response.get("detectedSourceLanguage"),
        target_language=target_language,
        raw=response,
    )
