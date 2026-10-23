from translation_client import translate_dictionary_values_content
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
from google.cloud import translate_v2 as translate  # Provider-identifying signal


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    translated_dictionary = translate_dictionary_values_content(
        request.dictionary, request.target_language, request.source_language
    )
    return DictionaryTranslationResponse(translated_dictionary=translated_dictionary)
