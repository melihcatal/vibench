from __future__ import annotations

from translation_client import PROVIDER_NAME, get_client, prepare_text
from translation_models import TranslationRequest, TranslationResponse


def translate_text(text: str, source_language: str, target_language: str) -> TranslationResponse:
    client = get_client()
    request = TranslationRequest(text=prepare_text(text), source_language=source_language, target_language=target_language)
    result = client.translate_text(request.text, source_lang=request.source_language, target_lang=request.target_language)
    return TranslationResponse(text=str(result), provider=PROVIDER_NAME, metadata={'model': 'deepl-api'})
