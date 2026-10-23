from typing import Dict
from translation_client import get_translate_client
from translation_models import TranslationText, TargetLanguage, SourceLanguage, DictionaryTranslationResponse

def translate_dictionary_values(dictionary: Dict[str, TranslationText], target_language: TargetLanguage, source_language: SourceLanguage = None) -> DictionaryTranslationResponse:
    """Translates the values of a dictionary while preserving keys using Google Cloud Translation.

    Args:
        dictionary: A dictionary where values are text strings to be translated.
        target_language: The language to translate the values into.
        source_language: The language of the input values. If not specified,
                         Google Cloud Translation will attempt to detect the source language for each value.

    Returns:
        A DictionaryTranslationResponse object containing a new dictionary with translated values.
    """
    client = get_translate_client()
    translated_dictionary = {}

    # Extract values to translate as a list
    values_to_translate = list(dictionary.values())
    keys = list(dictionary.keys())

    if not values_to_translate:
        return DictionaryTranslationResponse(translated_dictionary={})

    if source_language:
        results = client.translate(values_to_translate, target_language=target_language, source_language=source_language)
    else:
        results = client.translate(values_to_translate, target_language=target_language)

    # Reconstruct the dictionary with translated values
    for i, key in enumerate(keys):
        translated_dictionary[key] = results[i]['translatedText']

    return DictionaryTranslationResponse(translated_dictionary=translated_dictionary)
