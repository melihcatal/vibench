from typing import Dict, Any
from translation_client import get_azure_translator_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
    client = get_azure_translator_client()

    original_keys = list(request.dictionary.keys())
    original_values = [request.dictionary[key] for key in original_keys]

    text_elements = [{'Text': value} for value in original_values]

    azure_response = client.translate(
        text_elements=text_elements,
        source_language=request.source_language,
        target_language=request.target_language
    )

    translated_dictionary = {}
    if azure_response:
        for i, key in enumerate(original_keys):
            translated_value = ""
            if 'translations' in azure_response[i] and azure_response[i]['translations']:
                translated_value = azure_response[i]['translations'][0]['text']
            translated_dictionary[key] = translated_value

    return DictionaryTranslationResponse(
        translated_dictionary=translated_dictionary,
        source_language=request.source_language,
        target_language=request.target_language
    )
