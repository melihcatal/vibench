from typing import Dict, List
from translation_client import get_translation_client, get_gcp_project_id

def translate_dictionary_values(
    data: Dict[str, str], target_language_code: str, source_language_code: str
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary.

    Args:
        data: The dictionary with string values to translate.
        target_language_code: The ISO 639-1 code of the target language.
        source_language_code: The ISO 639-1 code of the source language.

    Returns:
        A new dictionary with the same keys and translated values.
    """
    if not data:
        return {}
        
    client = get_translation_client()
    project_id = get_gcp_project_id()

    keys = list(data.keys())
    values = list(data.values())
    
    response = client.translate_text(
        parent=f"projects/{project_id}",
        contents=values,
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )
    
    translated_values = [translation.translated_text for translation in response.translations]
    
    return dict(zip(keys, translated_values))
