from google.cloud import translate_v3
import os

def translate_appeal_text(
    project_id: str,
    text: str,
    target_language: str = "en",
    source_language: str = None
) -> str:
    """Translates text into the target language.

    Args:
        project_id: The ID of the Google Cloud project.
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "en").
        source_language: The language of the text to be translated (e.g., "es").
                         If None, the API will auto-detect the source language.
    Returns:
        The translated text.
    """

    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text
