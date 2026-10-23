from google.cloud import translate_v3 as translate

def translate_text_with_glossary(
    text: str,
    target_language_code: str,
    project_id: str,
    source_language_code: str = "en",
) -> str:
    """Translates text into the target language using a glossary.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        project_id: The ID of the Google Cloud project.
        source_language_code: The language code of the input text (defaults to "en" for English).

    Returns:
        The translated text.
    """

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"

    # Wrap the text in a list for the API call
    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",  # Can be "text/plain" or "text/html"
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
