from google.cloud import translate_v3 as translate

def translate_text(
    project_id: str,
    text_content: str,
    target_language: str,
    source_language: str = "en",
) -> str:
    """Translates text into the target language.

    Args:
        project_id: The ID of the GCP project.
        text_content: The text to translate.
        target_language: The language to translate to (e.g., "es" for Spanish).
        source_language: The language of the input text (defaults to "en").

    Returns:
        The translated text.
    """

    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text_content],
        mime_type="text/plain",  # Set to "text/html" for HTML input
        source_language_code=source_language,
        target_language_code=target_language,
    )

    # The Google Cloud Translation API returns a list of translations.
    # We expect only one translation for a single text_content input.
    if response.translations:
        return response.translations[0].translated_text
    return ""
