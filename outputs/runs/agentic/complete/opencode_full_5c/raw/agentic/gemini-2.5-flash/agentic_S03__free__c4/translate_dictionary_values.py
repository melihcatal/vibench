from translation_client import get_translation_client, get_project_id
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    client = get_translation_client()
    project_id = get_project_id()

    parent = f"projects/{project_id}/locations/global"

    original_values = list(request.dictionary.values())
    original_keys = list(request.dictionary.keys())

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": original_values,
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
            "mime_type": "text/plain",
        }
    )

    translated_values = [
        translation.translated_text for translation in response.translations
    ]
    translated_dictionary = dict(zip(original_keys, translated_values))

    return DictionaryTranslationResponse(translated_dictionary=translated_dictionary)
