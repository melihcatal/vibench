from typing import Dict
from google.cloud import translate_v2 as translate
from translation_client import get_translation_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    """Translates the values of a dictionary."""
    client = get_translation_client()
    
    if not request.data:
        return DictionaryTranslationResponse(translated_data={})

    keys = list(request.data.keys())
    values = list(request.data.values())
    
    translated_values_result = client.translate(
        values,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    
    translated_values = [item['translatedText'] for item in translated_values_result]
    
    translated_data = dict(zip(keys, translated_values))
    
    return DictionaryTranslationResponse(translated_data=translated_data)
