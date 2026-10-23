import os
from google.cloud import translate_v3 as translate
from security_client import get_google_cloud_translation_client


def translate_runbook_notes(
    project_id: str,
    text: str,
    target_language_code: str,
    source_language_code: str = "en",
) -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation.

    Args:
        project_id: The Google Cloud project ID.
        text: The text to translate.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        source_language_code: The language code of the input text. Defaults to "en".

    Returns:
        The translated text.
    """
    client = get_google_cloud_translation_client()
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",  # Mime types: "text/plain" or "text/html"
            source_language_code=source_language_code,
            target_language_code=target_language_code,
        )
        # Assuming only one text input for simplicity
        if response.translations:
            return response.translations[0].translated_text
        else:
            return ""
    except Exception as e:
        raise RuntimeError(
            f"Error translating text with Google Cloud Translation API: {e}"
        )
