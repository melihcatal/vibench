import os
from google.cloud import translate

def translate_text(text: str, target_language: str, project_id: str) -> str:
    """
    Translates text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.

    Raises:
        ValueError: If GOOGLE_APPLICATION_CREDENTIALS or project_id are not set.
        RuntimeError: For errors during the API call.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise as per Google Cloud client library documentation.
    # The client will automatically use the credentials configured in the environment.

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )

        if response.translations:
            return response.translations[0].translated_text
        else:
            return ""
    except Exception as e:
        raise RuntimeError(f"Error translating text with Google Cloud Translation API: {e}")

def translate_runbook_notes(notes: str, target_language: str, google_cloud_project_id: str) -> str:
    """
    Translates secret-rotation runbook notes into a specified target language.

    Args:
        notes: The runbook notes to translate.
        target_language: The language to translate the notes to (e.g., "fr" for French).
        google_cloud_project_id: The Google Cloud project ID where the Translation API is enabled.

    Returns:
        The translated runbook notes.
    """
    return translate_text(notes, target_language, google_cloud_project_id)
