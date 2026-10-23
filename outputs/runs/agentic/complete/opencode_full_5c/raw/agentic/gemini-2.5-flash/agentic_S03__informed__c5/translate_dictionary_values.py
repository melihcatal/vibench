from typing import Dict
from translation_client import get_translate_client
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
from google.cloud import translate_v3beta1 as translate


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    client = get_translate_client()
    parent = f"projects/{client.project}"

    original_values = list(request.dictionary.values())
    translated_values = []

    if not original_values:
        return DictionaryTranslationResponse(translated_dictionary={})

    response = client.translate_text(
        request=translate.TranslateTextRequest(
            parent=parent,
            contents=original_values,
            target_language_code=request.target_language,
            source_language_code=request.source_language
            if request.source_language
            else None,
            mime_type="text/plain",
        )
    )

    for translation in response.translations:
        translated_values.append(translation.translated_text)

    translated_dictionary = dict(zip(request.dictionary.keys(), translated_values))

    return DictionaryTranslationResponse(translated_dictionary=translated_dictionary)
