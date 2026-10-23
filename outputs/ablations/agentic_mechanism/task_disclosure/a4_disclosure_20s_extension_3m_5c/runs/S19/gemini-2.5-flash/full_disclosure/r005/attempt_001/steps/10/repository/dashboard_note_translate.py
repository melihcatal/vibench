from google.cloud import translate_v3 as translate

def translate_dashboard_note(
    text: str,
    target_language_code: str,
    project_id: str,
    source_language_code: str = "en"
) -> str:
    """Translates a given text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.
        source_language_code: The language code of the input text (e.g., "en" for English). Defaults to "en".

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set to "text/html" for HTML input
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    return response.translations[0].translated_text
