from google.cloud import translate_v3 as translate

def translate_alt_text(text: str, target_language: str = "en") -> str:
    """
    Translates generated image descriptions using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language for translation (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    project_id = "YOUR_PROJECT_ID"  # Replace with your Google Cloud Project ID
    location = "global"  # Or specify a different region if needed
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "mime_type": "text/plain",
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

