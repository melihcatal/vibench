from google.cloud import translate

def translate_text(text: str, target_language: str, project_id: str) -> str:
    """Translates a single text string between languages using Google Cloud Translation API.

    Args:
        text: The text string to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text string.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    # The Google Cloud Translation API might return multiple translations,
    # but for a single text string, we expect one.
    if response.translations:
        return response.translations[0].translated_text
    return ""

