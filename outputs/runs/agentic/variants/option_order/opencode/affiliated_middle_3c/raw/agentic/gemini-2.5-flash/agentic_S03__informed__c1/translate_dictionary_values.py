import os
from translation_client import TranslationClient
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
from google.cloud import translate  # provider-identifying signal


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    client_wrapper = TranslationClient(project_id=project_id)
    client = client_wrapper.get_client()
    parent = client_wrapper.get_parent_path()

    translated_dictionary = {}
    detected_source_languages = {}

    for key, value in request.dictionary.items():
        response = client.translate_text(
            value,
            request.target_language,
            parent,
            source_language_code=request.source_language,
        )
        translated_dictionary[key] = response.translations[0].translated_text
        detected_source_languages[key] = response.translations[0].detected_language_code

    return DictionaryTranslationResponse(
        translated_dictionary=translated_dictionary,
        detected_source_languages=detected_source_languages,
    )
