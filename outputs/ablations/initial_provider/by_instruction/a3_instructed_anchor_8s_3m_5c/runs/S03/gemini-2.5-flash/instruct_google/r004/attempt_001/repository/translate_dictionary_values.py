from google.cloud import translate_v3beta1 as translate
from typing import Dict, Optional

def translate_dictionary_values(
    project_id: str,
    dictionary: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None
) -> Dict[str, str]:
    """Translates dictionary values while preserving keys using Google Cloud Translation.

    Args:
        project_id: The ID of the GCP project.
        dictionary: A dictionary whose values are strings to be translated.
        target_language: The language to translate the text to (e.g., "es").
        source_language: The language of the input text (e.g., "en"). If None,
                         the API will attempt to detect the source language.

    Returns:
        A new dictionary with translated values and original keys.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    translated_dictionary = {}
    if not dictionary:
        return translated_dictionary

    # Extract values to translate
    values_to_translate = list(dictionary.values())
    keys = list(dictionary.keys())

    response = client.translate_text(
        parent=parent,
        contents=values_to_translate,
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/plain",
    )

    if response.translations:
        for i, translation in enumerate(response.translations):
            translated_dictionary[keys[i]] = translation.translated_text

    return translated_dictionary
