from google.cloud import translate_v3 as translate

def translate_single_text(text: str, target_language: str, project_id: str, source_language: str = None) -> str:
    """Translates a single piece of text.

    Args:
        text: The text to translate.
        target_language: The language to translate to.
        project_id: Your Google Cloud project ID.
        source_language: The language of the text. If not specified, auto-detected.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/plain",
    )

    return response.translations[0].translated_text
