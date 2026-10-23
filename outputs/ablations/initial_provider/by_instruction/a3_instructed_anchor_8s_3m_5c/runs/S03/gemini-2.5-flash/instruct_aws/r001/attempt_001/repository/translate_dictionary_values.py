import os
from deepl import Translator
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values_deepl(request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = Translator(auth_key)

    translated_dictionary = {}
    for key, value in request.dictionary.items():
        result = translator.translate_text(value, source_lang=request.source_language.upper(), target_lang=request.target_language.upper())
        translated_dictionary[key] = result.text

    return DictionaryTranslationResponse(translated_dictionary, request.source_language, request.target_language)
