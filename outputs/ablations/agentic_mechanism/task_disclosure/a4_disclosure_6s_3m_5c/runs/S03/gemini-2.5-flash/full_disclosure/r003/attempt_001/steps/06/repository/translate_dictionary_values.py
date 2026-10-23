import os
from google.cloud import translate_v3beta1 as translation_v3beta1

def translate_dictionary_values(dictionary, project_id, source_language_code, target_language_code):
    """Translates dictionary values while preserving keys using the Google Cloud Translation API.

    Args:
        dictionary (dict): A dictionary with string values to translate.
        project_id (str): The Google Cloud project ID.
        source_language_code (str): The source language code (e.g., "en-US").
        target_language_code (str): The target language code (e.g., "fr").

    Returns:
        dict: A new dictionary with the same keys and translated values.
    """
    client = translation_v3beta1.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translated_dictionary = {}
    for key, value in dictionary.items():
        if isinstance(value, str):
            response = client.translate_text(
                parent=parent,
                contents=[value],
                source_language_code=source_language_code,
                target_language_code=target_language_code,
            )
            # Assuming a single translation for a single content string
            translated_dictionary[key] = response.translations[0].translated_text
        else:
            translated_dictionary[key] = value  # Preserve non-string values

    return translated_dictionary
