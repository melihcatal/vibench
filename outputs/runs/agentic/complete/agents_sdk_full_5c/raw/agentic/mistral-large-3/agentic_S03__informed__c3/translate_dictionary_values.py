from typing import Dict
from translation_client import TranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
    client_helper = TranslationClient()
    client = client_helper.get_client()
    client_helper.validate_languages(request.source_lang, request.target_lang)

    translated_dict = {}
    for key, value in request.dictionary.items():
        result = client.translate_text(
            value,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        translated_dict[key] = result.text

    return DictionaryTranslationResponse(translated_dictionary=translated_dict)