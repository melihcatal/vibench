from __future__ import annotations

from translation_client import translate_text as deepl_translate_text
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_text(text: str, source_language: str, target_language: str) -> TranslationResult:
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=source_language,
        target_language=target_language,
    )
    payload = deepl_translate_text(request.text, request.source_language, request.target_language)
    return TranslationResult(
        translated_text=payload["translated_text"],
        source_language=request.source_language,
        target_language=request.target_language,
        provider=payload["provider"],
        metadata={"model": payload["model"], "detected_source_language": payload["detected_source_language"]},
    )
