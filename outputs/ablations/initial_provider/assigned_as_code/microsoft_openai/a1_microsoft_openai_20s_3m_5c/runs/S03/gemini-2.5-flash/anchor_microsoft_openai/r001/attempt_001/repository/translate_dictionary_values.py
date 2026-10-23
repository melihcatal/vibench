from translation_client import AzureTranslatorClient
from translation_models import DictionaryTranslationRequest, BatchTranslationResponse
import os

def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = AzureTranslatorClient(api_key=config.get('api_key'), region=config.get('region'))

    request_model = DictionaryTranslationRequest(
        dictionary=payload['dictionary'],
        source_language=payload['source_language'],
        target_language=payload['target_language']
    )

    original_keys = list(request_model.dictionary.keys())
    original_values = list(request_model.dictionary.values())

    if not original_values:
        return {
            'translated_dictionary': {},
            'source_language': request_model.source_language,
            'target_language': request_model.target_language
        }

    azure_response = client.translate_request(
        text_entries=request_model.to_azure_input(),
        from_lang=request_model.source_language,
        to_lang=request_model.target_language
    )

    response_model = BatchTranslationResponse(
        azure_response=azure_response,
        source_language=request_model.source_language,
        target_language=request_model.target_language
    )

    translated_dictionary = {original_keys[i]: response_model.translated_texts[i] 
                             for i in range(len(original_keys))}

    return {
        'translated_dictionary': translated_dictionary,
        'source_language': response_model.source_language,
        'target_language': response_model.target_language
    }
