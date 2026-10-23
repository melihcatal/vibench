"""
Translates dictionary values while preserving keys using Google Cloud Translation.
"""
from typing import Dict, List
from translation_client import get_translation_client

def translate_dict_values(
    data: Dict[str, str], 
    target_language: str, 
    source_language: str = "en"
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary.

    Args:
        data: A dictionary with string keys and string values to be translated.
        target_language: The ISO 639-1 code of the language to translate to.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A new dictionary with the same keys but with translated values.
    """
    if not data:
        return {}
        
    client = get_translation_client()
    
    keys = list(data.keys())
    values_to_translate = list(data.values())
    
    translation_results = client.translate(
        values=values_to_translate,
        target_language=target_language,
        source_language=source_language
    )
    
    translated_values = [result['translatedText'] for result in translation_results]
    
    return dict(zip(keys, translated_values))
