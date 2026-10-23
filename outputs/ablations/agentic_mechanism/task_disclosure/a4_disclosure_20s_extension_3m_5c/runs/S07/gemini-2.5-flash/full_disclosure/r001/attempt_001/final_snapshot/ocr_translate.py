from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str = "en") -> str:
    """Translates a given text using Google Cloud Translation.

    Args:
        text: The text to translate.
        project_id: The ID of the Google Cloud project.
        target_language: The language to translate the text into (e.g., "en" for English).

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

    # Assuming a single text input, return the first translation
    if response.translations:
        return response.translations[0].translated_text
    return text
