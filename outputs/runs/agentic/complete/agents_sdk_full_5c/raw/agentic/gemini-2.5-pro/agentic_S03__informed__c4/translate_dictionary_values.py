from translation_client import get_translation_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
    """
    Translates the string values of a dictionary, preserving the keys.

    Args:
        request: A DictionaryTranslationRequest object containing the data and languages.

    Returns:
        A DictionaryTranslationResponse object with the translated dictionary.
    """
    client = get_translation_client()
    
    if not request.data:
        return DictionaryTranslationResponse(translated_data={}, detected_source_language="N/A")

    original_keys = list(request.data.keys())
    values_to_translate = list(request.data.values())
    
    results = client.translate(
        values_to_translate,
        target_language=request.target_language,
        source_language=request.source_language if request.source_language != "auto" else ""
    )
    
    translated_data = {}
    detected_language = "N/A"
    if results:
        detected_language = results[0].get('detectedSourceLanguage', "N/A")

    for i, key in enumerate(original_keys):
        translated_data[key] = results[i]['translatedText']
        
    return DictionaryTranslationResponse(
        translated_data=translated_data,
        detected_source_language=detected_language
    )
