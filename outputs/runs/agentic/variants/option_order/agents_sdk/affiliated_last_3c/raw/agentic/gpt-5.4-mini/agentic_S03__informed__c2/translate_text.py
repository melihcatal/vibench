from __future__ import annotations

from translation_client import get_client, get_default_target_language
from translation_models import TranslationRequest, TranslationResponse, normalize_text

PROVIDER = "azure-ai-translation-text"


def translate_text(text: str, source_language: str, target_language: str | None = None) -> TranslationResponse:
    client = get_client()
    target = target_language or get_default_target_language()
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target),
    )
    results = client.translate(
        body=[request.text],
        to_language=[request.target_language],
        from_parameter=request.source_language or None,
    )
    translated = results[0].translations[0].text if results and results[0].translations else request.text
    return TranslationResponse(
        translated_text=translated,
        source_language=request.source_language,
        target_language=request.target_language,
        provider=PROVIDER,
    )
