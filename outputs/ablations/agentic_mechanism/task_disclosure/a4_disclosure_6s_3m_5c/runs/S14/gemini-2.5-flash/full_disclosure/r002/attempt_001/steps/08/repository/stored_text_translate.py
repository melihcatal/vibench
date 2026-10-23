from google.cloud import translate

def translate_text(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "en" for English).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
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

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
