from google.cloud import translate_v3 as translate

def translate_runbook_notes(project_id: str, text: str, target_language_code: str = "en") -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation API.

    Args:
        project_id: The Google Cloud project ID.
        text: The runbook notes text to translate.
        target_language_code: The language code to translate the text into (e.g., "en", "es", "fr").

    Returns:
        The translated text as a string.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or a specific region like 'us-central1'
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime type of the text input.
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return translated_text
