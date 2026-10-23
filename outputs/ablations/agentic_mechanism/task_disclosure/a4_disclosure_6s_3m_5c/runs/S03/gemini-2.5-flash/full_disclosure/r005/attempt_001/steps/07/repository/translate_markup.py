from google.cloud import translate_v3beta1 as translate

def translate_markup(text: str, source_language: str, target_language: str, project_id: str) -> str:
    """Translates HTML or markup text while preserving tags using Google Cloud Translation.

    Args:
        text: The HTML or markup text to translate.
        source_language: The language of the input text (e.g., "en").
        target_language: The language to translate the text to (e.g., "es").
        project_id: The Google Cloud project ID.

    Returns:
        The translated text with tags preserved.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        source_language_code=source_language,
        target_language_code=target_language,
        mime_type="text/html",  # Specify HTML to preserve tags
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
