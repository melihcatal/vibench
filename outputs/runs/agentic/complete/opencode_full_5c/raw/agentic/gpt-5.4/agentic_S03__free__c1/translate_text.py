from __future__ import annotations

from typing import Optional

from translation_client import DeepLTranslationClient
from translation_models import (
    TranslationRequest,
    TranslationResult,
    normalize_deepl_translation_response,
)


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> TranslationResult:
    client = DeepLTranslationClient()
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
    )
    response = client.translate(request.to_deepl_payload())
    normalized = normalize_deepl_translation_response(response)
    return TranslationResult(
        provider="DeepL",
        translated_text=normalized.translations[0] if normalized.translations else "",
        detected_source_language=normalized.detected_source_languages[0]
        if normalized.detected_source_languages
        else None,
        raw=response,
    )
