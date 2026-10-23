import os
from google.cloud import translate_v3 as translate

def translate_script(
    project_id: str,
    text: str,
    target_language_code: str,
    source_language_code: str = None
) -> str:
    """
    Translates a narration script using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # For global endpoint

    parent = f"projects/{project_id}/locations/{location}"

    # Wrap text in a list for the API call
    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
    )

    # The API can return multiple translations; we expect one for a single input text
    if response.translations:
        return response.translations[0].translated_text
    return text # Return original text if no translation found
