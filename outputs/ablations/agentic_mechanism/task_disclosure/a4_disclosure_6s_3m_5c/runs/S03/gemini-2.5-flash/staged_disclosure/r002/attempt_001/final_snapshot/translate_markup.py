from google.cloud import translate_v3 as translate

def translate_markup(text: str, target_language: str, project_id: str) -> str:
    """Translates HTML or markup text while preserving tags using Google Cloud Translation API.

    Args:
        text: The HTML or markup text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated HTML or markup text.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_html(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    return response.translations[0].translated_html
