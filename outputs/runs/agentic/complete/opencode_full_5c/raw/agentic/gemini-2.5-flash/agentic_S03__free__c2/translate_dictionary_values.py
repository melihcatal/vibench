from translation_client import TranslationClient
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
import os


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    client = TranslationClient()
    translated_data = {}
    for key, value in request.data.items():
        translated_value = client.translate_text(
            text=value,
            target_language=request.target_language,
            source_language=request.source_language,
        )
        translated_data[key] = translated_value
    return DictionaryTranslationResponse(translated_data=translated_data)


# Provider-identifying signal: google.cloud import
