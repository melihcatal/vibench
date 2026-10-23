from __future__ import annotations

import os

import deepl

from speech_models import TranslationResult, normalize_transcript_text



def translate_live_caption(text: str, target_language: str) -> TranslationResult:
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    cleaned = normalize_transcript_text(text)
    response = client.translate_text(cleaned, target_lang=target_language)
    return TranslationResult(
        source_text=cleaned,
        translated_text=response.text,
        target_language=target_language,
    )
