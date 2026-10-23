from typing import Dict
from translation_client import AzureTranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse, parse_azure_translation_response

def translate_dictionary_values(payload: DictionaryTranslationRequest, config=None) -> DictionaryTranslationResponse:
    client = AzureTranslationClient(api_key=config.get('api_key'), region=config.get('region'))
    
    original_keys = list(payload.dictionary.keys())
    original_values = list(payload.dictionary.values())

    if not original_values:
        return DictionaryTranslationResponse(
            translated_dictionary={},
            source_language=payload.source_language,
            target_language=payload.target_language
        )

    translated_data = client.translate(
        text_entries=original_values,
        from_lang=payload.source_language,
        to_lang=payload.target_language
    )
    
    translated_values = parse_azure_translation_response(translated_data)

    translated_dictionary = dict(zip(original_keys, translated_values))

    return DictionaryTranslationResponse(
        translated_dictionary=translated_dictionary,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
