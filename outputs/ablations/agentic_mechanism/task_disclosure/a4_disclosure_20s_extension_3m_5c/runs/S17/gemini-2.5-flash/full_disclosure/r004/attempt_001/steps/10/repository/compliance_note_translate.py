from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the Google Cloud project.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        source_language_code: The language code of the input text (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""
