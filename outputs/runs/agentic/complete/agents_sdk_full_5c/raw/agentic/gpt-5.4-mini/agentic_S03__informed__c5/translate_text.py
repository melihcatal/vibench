from __future__ import annotations

from translation_client import get_azure_translator_client
from translation_models import TranslationRequest, TranslationResult


def translate_text(source_language: str, target_language: str, text: str) -> TranslationResult:
    client = get_azure_translator_client()
    request = TranslationRequest(source_language=source_language, target_language=target_language, text=text)
    response = client.translate(body=[request.text], from_parameter=request.source_language, to=[request.target_language])
    translated = response[0].translations[0].text if response else ""
    detected = getattr(response[0].detected_language, "language", None) if response else None
    return TranslationResult(translated_text=translated, detected_source_language=detected, raw=response)
