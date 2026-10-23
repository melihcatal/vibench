from google.cloud import translate_v3 as translate

def translate_text_for_locale(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        project_id: The ID of the Google Cloud project.

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

    if response.translations:
        return response.translations[0].translated_text
    return text
