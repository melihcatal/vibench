from google.cloud import translate_v3 as translate

def translate_text_from_stored_document(
    project_id: str,
    text_content: str,
    target_language_code: str,
    source_language_code: str = None,
) -> str:
    """Translates text extracted from a stored document using Google Cloud Translation.

    Args:
        project_id: The Google Cloud project ID.
        text_content: The text content to translate.
        target_language_code: The language code to translate the text into (e.g., "en" for English).
        source_language_code: The language code of the input text (e.g., "es" for Spanish).
                               If not provided, Google Cloud Translation will attempt to auto-detect.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
            "mime_type": "text/plain",  # Mime type of the text input.
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text
