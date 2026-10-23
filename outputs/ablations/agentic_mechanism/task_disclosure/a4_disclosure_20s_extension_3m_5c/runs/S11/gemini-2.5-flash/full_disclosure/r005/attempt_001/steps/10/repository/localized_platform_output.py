import os
from google.cloud import translate_v2 as translate

def translate_platform_output(text: str, target_locale: str, project_id: str) -> dict:
    """
    Translates platform model output to a specified target locale using Google Cloud Translation API.

    Args:
        text: The text content from the platform model output to be translated.
        target_locale: The target language code for translation (e.g., "es" for Spanish, "fr" for French).
        project_id: The Google Cloud project ID.

    Returns:
        A dictionary containing the translated text and source language information.
    """
    translate_client = translate.Client(project=project_id)

    # Text can also be a list of strings, in which case this method returns a list of dictionaries.
    result = translate_client.translate(text, target_language=target_locale)

    return result
