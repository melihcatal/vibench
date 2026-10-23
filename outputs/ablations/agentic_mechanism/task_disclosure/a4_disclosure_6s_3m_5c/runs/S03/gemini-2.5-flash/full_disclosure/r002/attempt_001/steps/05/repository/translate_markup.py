from google.cloud import translate

def translate_markup(text: str, source_language: str, target_language: str, project_id: str) -> str:
    """Translates HTML or markup while preserving tags using Google Cloud Translation API.

    Args:
        text: The HTML or markup text to translate.
        source_language: The language of the input text (e.g., "en-US").
        target_language: The language to translate the text to (e.g., "es").
        project_id: The ID of the Google Cloud project.

    Returns:
        The translated HTML or markup text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/html",  # Specify that the text is HTML
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    # The Google Cloud Translation API handles HTML tag preservation automatically
    return response.translations[0].translated_text
