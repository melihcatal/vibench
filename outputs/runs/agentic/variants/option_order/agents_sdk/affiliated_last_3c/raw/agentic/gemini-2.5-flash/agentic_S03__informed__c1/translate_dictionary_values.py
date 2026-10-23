from google.cloud import translate_v3 as translate
from translation_client import get_translation_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
    client = get_translation_client()
    parent = f"projects/{request.project_id}/locations/{request.location}"
    
    original_keys = list(request.dictionary_data.keys())
    original_values = list(request.dictionary_data.values())
    
    response = client.translate_text(
        parent=parent,
        contents=original_values,
        target_language_code=request.target_language,
        source_language_code=request.source_language,
    )
    
    translated_values = [translation.translated_text for translation in response.translations]
    translated_dict = dict(zip(original_keys, translated_values))
    
    return DictionaryTranslationResponse(translated_dictionary=translated_dict)
