from __future__ import annotations

import os

import deepl

from speech_models import TranslationResult, normalize_transcript_text


def translate_live_caption(text: str, target_language: str) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing DEEPL_AUTH_KEY for DeepL API")
    translator = deepl.Translator(auth_key)
    normalized = normalize_transcript_text(text)
    response = translator.translate_text(normalized, target_lang=target_language)
    return TranslationResult(
        source_text=normalized,
        translated_text=response.text,
        target_language=target_language,
        detected_source_language=getattr(response, "detected_source_lang", None),
        raw={
            "billed_characters": getattr(response, "billed_characters", None),
            "provider": "DeepL",
        },
    )
