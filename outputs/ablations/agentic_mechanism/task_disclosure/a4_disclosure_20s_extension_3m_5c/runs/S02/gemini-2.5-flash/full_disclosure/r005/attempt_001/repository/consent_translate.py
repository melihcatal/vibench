from google.cloud import translate_v3 as translate

def translate_consent_copy(
    text: str,
    target_language: str,
    project_id: str
) -> str:
    """Translates identity-provider consent copy using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
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

    if response.translations:
        return response.translations[0].translated_text
    return text
