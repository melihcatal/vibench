from __future__ import annotations

from translation_client import get_client, normalize_language_code
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_text(text: str, source_language: str, target_language: str) -> TranslationResult:
    client = get_client()
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
    )
    response = client.translate(
        request.text,
        source_language=request.source_language,
        target_language=request.target_language,
        format_="text",
    )
    return TranslationResult(
        translated_text=response["translatedText"],
        source_language=request.source_language,
        target_language=request.target_language,
        metadata={"detected_source_language": response.get("detectedSourceLanguage")},
    )
