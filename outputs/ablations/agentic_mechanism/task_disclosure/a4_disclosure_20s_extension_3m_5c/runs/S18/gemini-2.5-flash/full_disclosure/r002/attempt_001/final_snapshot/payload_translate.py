from google.cloud import translate_v3 as translate

def translate_text(
    project_id: str,
    text: str,
    target_language_code: str,
    source_language_code: str = "en",
) -> str:
    """Translates text into the target language.

    Args:
        project_id: The Google Cloud project ID.
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        source_language_code: The language code of the input text (defaults to "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    translated_text = response.translations[0].translated_text
    return translated_text
