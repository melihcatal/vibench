from translation_client import get_translation_client, get_gcp_project_id

def translate_text(text: str, target_language: str, source_language: str) -> str:
    """
    Translates a single string of text.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        The translated text.
    """
    client = get_translation_client()
    project_id = get_gcp_project_id()
    
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/plain",
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
