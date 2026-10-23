from google.cloud import translate_v3 as translate

def translate_onboarding_copy(text: str, target_language: str, project_id: str) -> str:
    """Translates onboarding copy into the user's locale using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

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

