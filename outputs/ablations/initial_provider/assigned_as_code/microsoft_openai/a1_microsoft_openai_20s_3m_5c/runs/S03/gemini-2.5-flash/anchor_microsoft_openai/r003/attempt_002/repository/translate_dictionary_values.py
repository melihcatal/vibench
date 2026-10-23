from typing import Dict, Any, List
from translation_client import get_azure_translation_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(payload: DictionaryTranslationRequest, config: Dict[str, str] = None) -> DictionaryTranslationResponse:
    client = get_azure_translation_client(config or {})
    
    # Prepare texts for translation: only values are translated
    values_to_translate = []
    original_keys = []
    for key, value in payload.dictionary.items():
        values_to_translate.append({'Text': value})
        original_keys.append(key)
    
    azure_response = client.translate(
        texts=values_to_translate,
        from_lang=payload.source_language,
        to_lang=payload.target_language
    )
    
    translated_dictionary = {}
    for i, item in enumerate(azure_response):
        original_key = original_keys[i]
        translated_value = ""
        if 'translations' in item and item['translations']:
            translated_value = item['translations'][0]['text']
        translated_dictionary[original_key] = translated_value

    return DictionaryTranslationResponse(
        dictionary=translated_dictionary,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
