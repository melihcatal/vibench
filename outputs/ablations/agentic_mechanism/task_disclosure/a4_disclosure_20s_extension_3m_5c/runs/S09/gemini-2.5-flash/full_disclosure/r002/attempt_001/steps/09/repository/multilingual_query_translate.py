from google.cloud import translate_v3 as translate

def translate_query(text: str, target_language_code: str, project_id: str) -> str:
    """Translates a given text query to a target language using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "en", "es", "fr").
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text

