from google.cloud import translate_v3 as translate

def translate_text(
    project_id: str,
    text: str,
    target_language: str,
    source_language: str = "en",
) -> str:
    """Translates text into the target language.

    Args:
        project_id: The ID of the Google Cloud project.
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        source_language: The language of the input text (defaults to "en").

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
            "source_language_code": source_language,
        }
    )

    return response.translations[0].translated_text
