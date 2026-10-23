import os
from google.cloud import translate_v3 as translate

def translate_narration_script(text: str, target_language_code: str, project_id: str, source_language_code: str = None) -> str:
    """Translates narration scripts using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text into (e.g., "es").
        project_id: Your Google Cloud project ID.
        source_language_code: Optional. The language code of the input text (e.g., "en").
                              If not specified, the API will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set to "text/html" for HTML content.
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
