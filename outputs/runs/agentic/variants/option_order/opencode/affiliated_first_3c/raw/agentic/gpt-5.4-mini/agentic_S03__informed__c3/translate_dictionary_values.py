from __future__ import annotations

from translation_client import PROVIDER_NAME, get_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse


def translate_dictionary_values(values, source_language: str, target_language: str) -> DictionaryTranslationResponse:
    client = get_client()
    request = DictionaryTranslationRequest(values=dict(values), source_language=source_language, target_language=target_language)
    translated = {
        key: str(client.translate_text(value, source_lang=request.source_language, target_lang=request.target_language))
        for key, value in request.values.items()
    }
    return DictionaryTranslationResponse(values=translated, provider=PROVIDER_NAME, metadata={'model': 'deepl-api'})
