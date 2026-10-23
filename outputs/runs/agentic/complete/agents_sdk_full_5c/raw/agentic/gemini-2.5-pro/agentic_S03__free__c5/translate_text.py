from translation_client import get_translation_client, get_gcp_project_id

def translate_text(text: str, target_language_code: str, source_language_code: str) -> str:
    """
    Translates a single text string to a target language using Google Cloud Translate.

    Args:
        text: The text to translate.
        target_language_code: The ISO 639-1 code of the target language.
        source_language_code: The ISO 639-1 code of the source language.

    Returns:
        The translated text.
    """
    client = get_translation_client()
    project_id = get_gcp_project_id()
    
    response = client.translate_text(
        parent=f"projects/{project_id}",
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )
    
    return response.translations[0].translated_text
