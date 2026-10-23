from google.cloud import translate

def translate_invoice_note(text: str, project_id: str, target_language: str = "en") -> str:
    """Translates a given text using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        project_id: The Google Cloud project ID.
        target_language: The language to translate the text into (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    return response.translations[0].translated_text

