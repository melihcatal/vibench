from google.cloud import translate_v3 as translate

def translate_transcript(text: str, target_language_code: str, project_id: str) -> str:
    """Translates transcript segments using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text into (e.g., "es").
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    # The parent format is "projects/{project_id}/locations/{location_id}"
    # For global location, use "global"
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    # Assuming only one text input, get the first translation
    return response.translations[0].translated_text
