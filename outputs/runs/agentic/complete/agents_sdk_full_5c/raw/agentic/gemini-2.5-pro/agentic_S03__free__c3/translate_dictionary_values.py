from typing import Dict, List
from translation_client import get_translation_client

def translate_dictionary_values(
    data: Dict[str, str], target_language_code: str, source_language_code: str = "en-US"
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary.

    Args:
        data: A dictionary with string keys and string values to be translated.
        target_language_code: The ISO 639-1 language code for translation.
        source_language_code: The ISO 639-1 language code of the source text.

    Returns:
        A new dictionary with original keys and translated values.
    """
    if not data:
        return {}

    client, parent = get_translation_client()
    
    original_keys = list(data.keys())
    values_to_translate = list(data.values())

    response = client.translate_text(
        parent=parent,
        contents=values_to_translate,
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/plain",
    )

    translated_values = [t.translated_text for t in response.translations]

    return dict(zip(original_keys, translated_values))
