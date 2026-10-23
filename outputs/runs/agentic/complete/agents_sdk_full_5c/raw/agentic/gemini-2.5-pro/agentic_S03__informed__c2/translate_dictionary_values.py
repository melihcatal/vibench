from typing import Dict
from translation_client import get_translation_client
from translation_models import DictionaryTranslationResponse

def translate_dictionary_values(
    data: Dict[str, str], target_language: str, source_language: str = None
) -> DictionaryTranslationResponse:
    """
    Translates the string values of a dictionary.

    Args:
        data: A dictionary with string keys and string values to be translated.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language. Optional.

    Returns:
        A DictionaryTranslationResponse with the translated dictionary.
    """
    if not data:
        return DictionaryTranslationResponse(translated_dictionary={})

    client = get_translation_client()
    
    keys = list(data.keys())
    values_to_translate = list(data.values())

    translation_results = client.translate(
        values_to_translate,
        target_language=target_language,
        source_language=source_language or '',
    )
    
    translated_values = [res['translatedText'] for res in translation_results]
    
    # Assuming all items have the same detected source language, return the first one.
    detected_lang = None
    if translation_results:
        detected_lang = translation_results[0].get('detectedSourceLanguage')

    translated_dict = dict(zip(keys, translated_values))

    return DictionaryTranslationResponse(
        translated_dictionary=translated_dict,
        detected_source_language=detected_lang
    )
