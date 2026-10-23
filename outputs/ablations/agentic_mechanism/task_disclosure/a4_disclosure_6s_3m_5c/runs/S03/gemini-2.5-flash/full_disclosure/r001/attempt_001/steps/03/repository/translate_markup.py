from google.cloud import translate_v3beta1 as translate

def translate_markup(text: str, target_language: str, project_id: str) -> str:
    """Translates HTML or markup while preserving tags using Google Cloud Translation API.

    Args:
        text: The HTML or markup text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text with tags preserved.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        mime_type="text/html",  # Specify that the text is HTML
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
