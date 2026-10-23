from google.cloud import translate

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """
    Translates text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate to (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
