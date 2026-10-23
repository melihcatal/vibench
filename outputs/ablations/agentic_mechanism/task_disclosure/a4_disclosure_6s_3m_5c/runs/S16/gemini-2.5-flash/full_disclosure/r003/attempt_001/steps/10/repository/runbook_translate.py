from google.cloud import translate_v3 as translate

def translate_runbook_notes(text: str, target_language: str = "en", project_id: str = "your-gcp-project-id"):
    """Translates secret-rotation runbook notes using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language: The language to translate the text into (e.g., "en" for English).
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""
