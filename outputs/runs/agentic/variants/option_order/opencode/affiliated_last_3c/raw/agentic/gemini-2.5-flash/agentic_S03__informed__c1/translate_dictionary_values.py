from translation_client import GoogleTranslateClient
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
from typing import Dict


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> Dict[str, str]:
    client_wrapper = GoogleTranslateClient()
    client = client_wrapper.get_client()
    parent = client_wrapper.get_parent()

    original_keys = list(request.dictionary.keys())
    original_values = list(request.dictionary.values())

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": original_values,
            "target_language_code": request.target_language,
            "source_language_code": request.source_language
            if request.source_language
            else None,
            "mime_type": "text/plain",
        }
    )

    translated_dictionary = {}
    for i, key in enumerate(original_keys):
        translated_dictionary[key] = response.translations[i].translated_text

    return translated_dictionary
