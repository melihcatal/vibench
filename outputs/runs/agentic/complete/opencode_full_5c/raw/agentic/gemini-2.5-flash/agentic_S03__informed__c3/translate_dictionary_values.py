from translation_client import TranslationClient
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    client = TranslationClient()
    translate_client = client.get_client()
    parent = client.get_parent()

    keys = list(request.dictionary.keys())
    values = list(request.dictionary.values())

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": values,
            "target_language_code": request.target_language,
            "source_language_code": request.source_language,
            "mime_type": request.mime_type,
        }
    )

    translated_dictionary = {
        keys[i]: translation.translated_text
        for i, translation in enumerate(response.translations)
    }
    detected_source_languages = {
        keys[i]: translation.detected_language_code
        for i, translation in enumerate(response.translations)
    }

    return DictionaryTranslationResponse(
        translated_dictionary, detected_source_languages
    )
